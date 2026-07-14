import os
import sys
import urllib
import collections
import functools
import json
import datetime
import re
import requests
from bs4 import BeautifulSoup
import pytest

#Egor
#=======================================================================#

class CSVReaderMixin:
    def _read_csv_file(self, file_path, field_names, has_header=True, limit=1000):
        results = []

        with open(file_path, 'r', encoding='utf8') as f:
            if has_header:
                next(f)
            for i, line in enumerate(f):
                if i >= limit:
                    break
                l = line.strip().split(',')
                row = {}
                for field, dtype, index_list in field_names:
                    value = l[index_list]
                    if dtype == str:
                        row[field] = value
                    elif dtype == int:
                        row[field] = int(value)
                    elif dtype == float:
                        row[field] = float(value)
                    elif dtype == datetime.datetime:
                        row[field] = datetime.datetime.fromtimestamp(int(value))
                results.append(row)

        return results

class CheckExistFileMixin:
    @staticmethod
    def _check_exist_file(file_path, check_filenames):
        """
        Проверка существования необходимых файлов
        """
        file_name = os.path.basename(file_path)
        if not (os.path.exists(file_path) and os.path.isfile(file_path)):
            raise FileNotFoundError(f"Таких путей или файлов не существует {file_path}")
        if file_name not in check_filenames:
            raise FileNotFoundError(f"Необходим файл {','.join(check_filenames)}, а был выбран {file_name}")
        return file_path

class CheckArgumentFunctionMixin:
    @staticmethod
    def _check_count_n(result, n):
        """
        Проверка сущетсвование вхождения индекса в списке
        """
        if n < 1 or n > len(result):
            raise IndexError(f"Не существует такого количество фильмов {n}")

        return dict(list(result)[:n])

class Ratings(CSVReaderMixin, CheckExistFileMixin):
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, file_ratings, file_movies, is_header=True, limit=1000):
        """
        Заполните здесь любые поля, которые, по вашему мнению, вам понадобятся.
        """
        self.file_ratings = self._check_exist_file(file_ratings, ['ratings.csv'])
        self.file_movies = self._check_exist_file(file_movies, ['movies.csv'])
        self.is_header = is_header
        self.limit = limit
        self.ratings = self.read_csv_ratings()
        self.movies = self.read_csv_movies()

    def read_csv_ratings(self):
        """
        Прочтение файла и составление необходимого формата для чтения данных
        """
        blank = [
            ('userId', int, 0),
            ('movieId', int, 1),
            ('rating', float, 2),
            ('timestamp', datetime.datetime, 3),
        ]
        return self._read_csv_file(self.file_ratings, blank, has_header=self.is_header, limit=self.limit)

    def read_csv_movies(self):
        """
        Прочтение файла и составление необходимого формата для чтения данных
        """
        blank = [
            ('movieId', int, 0),
            ('title', str, 1),
            ('genres', str, 2),
        ]
        return self._read_csv_file(self.file_movies, blank, has_header=self.is_header, limit=self.limit)

    class Movies(CheckArgumentFunctionMixin):
        def __init__(self, ratings, movies_csv = None):
            self.ratings = ratings
            self.movies_csv = movies_csv
            self.movies_db = self._read_csv_movies_foreign_key()

        def dist_by_year(self):
            """
            Метод возвращает словарь, где ключи — это годы, а значения — это количества.
            Отсортируйте его по возрастанию лет. Вам нужно извлечь годы из временных меток.
            """
            ratings_by_year = {}
            for row in self.ratings:
                year = row['timestamp'].year
                ratings_by_year[year] = ratings_by_year.get(year, 0) + 1
                # ratings_by_year[year] += 1
            return dict(sorted(ratings_by_year.items()))

        def dist_by_rating(self):
            """
            Метод возвращает словарь, где ключи — это рейтинги, а значения — это счетчики.
            Сортируйте его по возрастанию рейтингов.
            """
            ratings_distribution = {}
            for row in self.ratings:
                rat = row['rating']
                ratings_distribution[rat] = ratings_distribution.get(rat, 0) + 1
            return dict(sorted(ratings_distribution.items()))

        def top_by_num_of_ratings(self, n):
            """
            Метод возвращает top-n фильмов по количеству оценок.
            Это словарь, где ключами являются названия фильмов, а значениями — числа.
            Сортируйте его по числам в порядке убывания.
            """
            top_movies ={}
            for row in self.ratings:
                movie = row['movieId']
                top_movies[movie] = top_movies.get(movie, 0) + 1
                # top_movies[movie] += 1

            return self.__preparation_response(sorted(top_movies.items(), key=lambda x: x[1], reverse=True), n)

        def top_by_ratings(self, n, metric='average'):
            """
            Метод возвращает топ-n фильмов по среднему или медианному значению рейтингов.
            Это словарь, где ключами являются названия фильмов, а значениями — значения метрик.
            Сортируйте его по убыванию метрик.
            Значения должны быть округлены до 2 десятичных знаков.
            """
            top_movies = {}
            movies_ratings = {}

            for row in self.ratings:
                movie = row['movieId']
                if movie not in movies_ratings:
                    movies_ratings[movie] = []
                movies_ratings[movie].append(row['rating'])

            for movie, ratings in movies_ratings.items():
                if metric == 'average':
                    top_movies[movie] = self._mean(ratings)
                elif metric == 'median':
                    top_movies[movie] = self._median(ratings)
                else:
                    raise Exception("Задана не правильная метрика")

            return self.__preparation_response(sorted(top_movies.items(), key=lambda x: x[1], reverse=True), n)

        def top_controversial(self, n):
            """
            Метод возвращает top-n фильмов по дисперсии рейтингов.
            Это словарь, где ключами являются названия фильмов, а значениями — дисперсии.
            Сортируйте его по дисперсии по убыванию.
            Значения должны быть округлены до 2 десятичных знаков.
            """
            top_movies = {}
            movie_ratings = collections.defaultdict(list)
            for row in self.ratings:
                movie_ratings[row['movieId']].append(row['rating'])

            top_movies = self._dispersion(movie_ratings, top_movies)

            return self.__preparation_response(sorted(top_movies.items(), key=lambda x: x[1], reverse=True), n)

        def count_ratings_per_movie(self):
            """
            Возвращает словарь с количеством оценок на каждый фильм (movieId).
            """
            movie_count = collections.defaultdict(int)
            for row in self.ratings:
                movie_count[row['movieId']] += 1
            return self.__preparation_response(sorted(movie_count.items(), key=lambda x: x[1], reverse=True), 10)

        def count_unique_movies_by_genre_top_five(self):
            """
            Возвращает словарь с количеством уникальных фильмов по жанрам.
            """
            genre_count = collections.defaultdict(int)
            for movie in self.movies_db.values():
                for genre in movie['genres'].split('|'):
                    genre_count[genre] += 1
            return dict(list(sorted(genre_count.items(), key=lambda x: x[1], reverse=True))[:5])

        def __preparation_response(self, movie_ratings, n):
            return self.__get_dict_title_by_movie_id(self._check_count_n(movie_ratings, n))

        def __get_dict_title_by_movie_id(self, movie_id_count):
            """
            Получение по id фильма его название и возврата словаря
            """
            res_fin = {}

            for movieId, count in movie_id_count.items():
                try:
                    if not self.movies_db:
                        raise Exception("Не возможно выводить данные необходимо данные movies_db")
                    title = self.movies_db[movieId]['title']
                except KeyError:
                    print(f"Не существует ключа в таблице movies.csv {movieId}")
                    continue
                res_fin[title] = count

            return res_fin

        def _read_csv_movies_foreign_key(self):
            """
            Преобразует данные из read_csv_movies() в словарь с movieId как ключом.
            """
            if self.movies_csv:
                return {movie['movieId']: {'title': movie['title'], 'genres': movie['genres']}
                        for movie in self.movies_csv}
            return None

        @staticmethod
        def _mean(ratings):
            """
            Получение среднего значения
            """
            return round(sum(ratings) / len(ratings), 2)

        @staticmethod
        def _median(ratings):
            """
            Получение медианного значения
            """
            sorted_ratings = sorted(ratings)
            n = len(sorted_ratings)
            mid = n // 2
            if n % 2 == 1:
                return round(sorted_ratings[mid], 2)
            return round((sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2, 2)

        def _dispersion(self, data, result):
            """
            Подсчет дисперсии
            """
            for movie, ratings in data.items():
                result[movie] = round(sum((xi - self._mean(ratings)) ** 2 for xi in ratings) / len(ratings), 2)
            return result



    class Users(Movies):
        """
        В этом классе должны работать три метода.
        Наследуется от класса Movies. Несколько методов похожи на методы из него.
        """
        def __init__(self, ratings):
            super().__init__(ratings)
            self.ratings = ratings

        def dist_by_rating(self):
            """
            Возвращает распределение пользователей по количеству оценок, которые они поставили.
            """
            top_users = collections.defaultdict(list)
            for row in self.ratings:
                top_users[row['userId']].append(row['rating'])
            return {user_id: len(value) for user_id, value in top_users.items()}

        def top_by_rating(self, metric='average'):
            """
            Возвращает распределение пользователей по средним или медианным оценкам, которые они поставили.
            """
            top_users = collections.defaultdict(list)
            result = {}
            for row in self.ratings:
                top_users[row['userId']].append(row['rating'])

            for user_id, values in top_users.items():
                if metric == 'average':
                    result[user_id] = self._mean(values)
                elif metric == 'median':
                    result[user_id] = self._median(values)
                else:
                    raise Exception("Нет такой метрики")

            return result

        def top_controversial(self, n):
            """
            Возвращает n лучших пользователей с самой большой дисперсией их оценок.
            """
            top_users = {}
            movie_ratings = collections.defaultdict(list)
            for row in self.ratings:
                movie_ratings[row['userId']].append(row['rating'])

            top_users = self._dispersion(movie_ratings, top_users)

            return self._check_count_n(sorted(top_users.items(), key=lambda x: x[1], reverse=True), n)


class Tags(CSVReaderMixin, CheckExistFileMixin, CheckArgumentFunctionMixin):
    """
    Analyzing data from tags.csv
    """

    def __init__(self, file_tags, is_header=True, limit=1000):
        """
        Put here any fields that you think you will need.
        """
        self.file_tags = self._check_exist_file(file_tags, ['tags.csv'])
        self.is_header = is_header
        self.limit = limit
        self.tags_csv = self._read_csv_tags()

    def _read_csv_tags(self):
        blank = [
            ('userId', int, 0),
            ('movieId', int, 1),
            ('tag', str, 2),
            ('timestamp', datetime.datetime, 3),
        ]
        return self._read_csv_file(self.file_tags, blank, self.is_header, self.limit)

    def most_words(self, n):
        """
         Метод возвращает top-n тегов с наибольшим количеством слов внутри.
          Это словарь, где ключи — теги, а значения — количество слов внутри тега.
        Удалить дубликаты. Сортировать по номерам по убыванию.
        """
        big_tags = collections.defaultdict(int)
        for row in self.tags_csv:
            text_tags = row['tag']
            big_tags[text_tags] = len(text_tags.split(' '))


        return self._check_count_n(sorted(big_tags.items(), key=lambda x: x[1], reverse=True), n)

    def longest(self, n):
        """
        Метод возвращает top-n самых длинных тегов по количеству символов.
         Это список тегов. Удалите дубликаты. Отсортируйте его по номерам в порядке убывания.
        """
        big_tags = collections.defaultdict(int)
        for row in self.tags_csv:
            text_tags = row['tag']
            big_tags[text_tags] = len(text_tags.replace(' ', ''))

        return list(self._check_count_n(sorted(big_tags.items(), key=lambda x: x[1], reverse=True), n).keys())

    def most_words_and_longest(self, n):
        """
        Метод возвращает пересечение между верхними n тегами с наибольшим количеством слов внутри и верхними
         n самыми длинными тегами по количеству символов.
        Удаляем дубликаты. Это список тегов.
        """
        return list(set(self.most_words(n)).intersection(set(self.longest(n))))

    def most_popular(self, n):
        """
        Метод возвращает самые популярные теги.
        Это словарь, где ключи — теги, а значения — счетчики.
        Удалите дубликаты. Отсортируйте по счетчикам по убыванию.
        """
        popular_tags = collections.defaultdict(int)
        for row in self.tags_csv:
            text_tags = row['tag']
            popular_tags[text_tags] += 1

        return self._check_count_n(sorted(popular_tags.items(), key=lambda x: x[1], reverse=True), n)

    def tags_with(self, word):
        """
        Метод возвращает все уникальные теги, которые включают слово, указанное в качестве аргумента.
        Удалить дубликаты. Это список тегов. Отсортировать его по именам тегов в алфавитном порядке.
        """
        tags_with_word = {}
        for row in self.tags_csv:
            text_tags = row['tag']
            if word.lower() in [w.lower() for w in text_tags.split(' ')]:
                tags_with_word[text_tags.lower()] = text_tags
        return sorted(tags_with_word.values())

    def tags_starting_with_letter(self, letter):
        """
        Возвращает список уникальных тегов, начинающихся на указанную букву (регистр не учитывается).
        """
        tags = set()
        for row in self.tags_csv:
            tag = row['tag']
            if tag.lower().startswith(letter.lower()):
                tags.add(tag)
        return sorted(tags)


#Timur
#=========================================================================#


class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file_links, movies_file_path):
        self.file_links = path_to_the_file_links
        self.file_movies = movies_file_path
        self.is_header = True
        self.movies_data = self._load_and_combine_data()
        
    def _load_and_combine_data(self):
        """Загружает и объединяет данные из обоих файлов с валидацией"""
        combined_data = {}
        max_lines = 1000
        
        def validate_header(file_obj, expected_header):
            header = file_obj.readline().strip()
            if header != expected_header:
                raise ValueError(f"Invalid header. Expected: '{expected_header}', got: '{header}'")
            return header

        with open(self.file_links, 'r', encoding='utf-8') as f:
            if self.is_header:
                try:
                    validate_header(f, "movieId,imdbId,tmdbId")
                except ValueError as e:
                    raise ValueError(f"Invalid links.csv header: {str(e)}")

            for line_num, line in enumerate(f, 1):
                if line_num > max_lines:
                    break

                parts = line.strip().split(',')
                if len(parts) < 2:
                    raise ValueError(f"links.csv line {line_num}: expected at least 2 columns, got {len(parts)}")

                try:
                    movie_id = int(parts[0])
                    if movie_id <= 0:
                        raise ValueError(f"links.csv line {line_num}: movieId must be positive integer")
                except ValueError:
                    raise ValueError(f"links.csv line {line_num}: invalid movieId format (must be integer)")

                imdb_id = parts[1]
                if not (imdb_id.isdigit() and len(imdb_id) >= 3):
                    raise ValueError(f"links.csv line {line_num}: invalid imdbId format (expected tt followed by digits)")

                tmdb_id = parts[2].strip() if len(parts) > 2 else None  
                if tmdb_id:
                    if not tmdb_id.isdigit():
                        raise ValueError(f"links.csv line {line_num}: invalid tmdbId format (must be integer or empty)")
                    tmdb_id = int(tmdb_id)
                else:
                    tmdb_id = None

                combined_data[movie_id] = {
                    'imdbId': imdb_id,
                    'tmdbId': int(tmdb_id) if tmdb_id else None
                }

        with open(self.file_movies, 'r', encoding='utf-8') as f:
            if self.is_header:
                try:
                    validate_header(f, "movieId,title,genres")
                except ValueError as e:
                    raise ValueError(f"Invalid movies.csv header: {str(e)}")

            for line_num, line in enumerate(f, 1):
                if line_num > max_lines:
                    break

                try:
                    parts = self._parse_movie_line(line)
                except Exception as e:
                    raise ValueError(f"movies.csv line {line_num}: parsing error - {str(e)}")

                if len(parts) != 3:
                    raise ValueError(f"movies.csv line {line_num}: expected exactly 3 columns, got {len(parts)}")

                try:
                    movie_id = int(parts[0])
                    if movie_id <= 0:
                        raise ValueError("movieId must be positive integer")
                except ValueError:
                    raise ValueError(f"movies.csv line {line_num}: invalid movieId format (must be integer)")

                title = parts[1].strip()
                if not title or len(title) < 1:
                    raise ValueError(f"movies.csv line {line_num}: title cannot be empty")
                
                genres = parts[2].strip()
                if not genres:
                    genres = "(no genres listed)" 

                if movie_id in combined_data:
                    combined_data[movie_id]['title'] = title
                    combined_data[movie_id]['genres'] = genres

        return combined_data
    
    def _parse_movie_line(self, line):
        """Парсит строку из movies.csv с учетом кавычек"""
        parts = [""] * 3
        in_quotes = False
        index = 0
        for char in line:
            if char == '\"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                index += 1
            else:
                parts[index] += char
        return parts

    def first_n_movie_id(self,n):
        return list(self.movies_data.keys())[:n]


#функции для парсинга (начало)    
    def get_imdb(self, list_of_movies, list_of_fields):
        """
Метод возвращает список списков [MovieID, field1, field2, field3, ...] для списка фильмов, указанного в качестве аргумента (MovieID).
Например, [MovieID, режиссер, бюджет, Совокупный мировой кассовый сбор, продолжительность].
Значения должны быть взяты с веб-страниц фильмов на IMDB.
Отсортируйте их по идентификатору фильма в порядке убывания.
        """
        imdb_info = []
        
        for movie_id in list_of_movies:
            try:
                if movie_id not in self.movies_data:
                    raise ValueError(f"Фильм с ID {movie_id} не найден в локальных данных")
                
                movie_data = self._parse_movie(movie_id, list_of_fields)
                if movie_data:
                    imdb_info.append(movie_data)
                
            except Exception as e:
                print(f"Ошибка при обработке фильма {movie_id}: {str(e)}")
                continue
        
        imdb_info.sort(key=lambda x: x[0], reverse=True)
        self.imdb_info = imdb_info
        return imdb_info
    
    def _parse_movie(self, movie_id, fields):
        imdb_id = self.movies_data[movie_id]['imdbId']
        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept-Language': 'en-US,en;q=0.5'
            }, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if "404" in soup.title.text:
                raise ValueError(f"Страница фильма {movie_id} не найдена на IMDB")
            
            field_handlers = {
                'Director': self._get_director,
                'Budget': self._get_budget,
                'Cumulative Worldwide Gross': self._get_gross,
                'Runtime': self._get_runtime
            }
            
            movie_data = [movie_id]
            for field in fields:
                if field not in field_handlers:
                    raise ValueError(f"Поле {field} не поддерживается")
                movie_data.append(field_handlers[field](soup))
            
            return movie_data
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Ошибка сети: {str(e)}")
        
    def _get_director(self, soup):
        director_link = soup.find('a', class_='ipc-metadata-list-item__list-content-item', href=lambda x: x and 'name' in x)
        if director_link:
            return director_link.text.strip()
    
        return "N/A"

    def _get_budget(self, soup):
        budget_section = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
        if budget_section:
            budget_text = budget_section.find('span', class_='ipc-metadata-list-item__list-content-item').text.strip()

            budget_num = ''.join(c for c in budget_text if c.isdigit())
            return int(budget_num) if budget_num else 0
        return None

    def _get_gross(self, soup):
        gross_section = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
        if gross_section:
            gross_text = gross_section.find('span', class_='ipc-metadata-list-item__list-content-item').text.strip()

            gross_num = ''.join(c for c in gross_text if c.isdigit())
            return int(gross_num) if gross_num else 0
        return 0

    def _get_runtime(self, soup):
        runtime_section = soup.find('li', {'data-testid': 'title-techspec_runtime'})
        if runtime_section:
            runtime_text = runtime_section.find('div').text.strip()
            total_minutes = 0

        if 'hour' in runtime_text:
            hour_part = runtime_text.split('hour')[0].strip()
            hours = int(hour_part) if hour_part.isdigit() else 0
            total_minutes += hours * 60
        
        if 'minute' in runtime_text:
            minute_part = runtime_text.split('minute')[0].split()[-1].strip()
            minutes = int(minute_part) if minute_part.isdigit() else 0
            total_minutes += minutes

        return datetime.timedelta(minutes=total_minutes) if total_minutes > 0 else None
#(конец)


    def top_directors(self, n):
        """
Метод возвращает dict из топ-n режиссеров, где ключами являются режиссеры, а
значениями - количесвто созданных ими фильмов. Отсортируйте его по убыванию количества.
        """
        directors = {}
        for movie in self.imdb_info:
            directors[movie[1]] = directors.get(movie[1], 0) + 1

        directors = dict(sorted(directors.items(), key = lambda item: item[1], reverse=True)[:n])

        return directors
        
    def most_expensive(self, n):
        """
Метод возвращает dict с топовыми фильмами, где ключами являются названия фильмов, а
значениями - их бюджеты. Отсортируйте его по убыванию бюджетов.
        """
        budgets = {}
        for movie in self.imdb_info:
            movie_name = self.movies_data[movie[0]]['title']
            if movie[2] is not None:
                budgets[movie_name] = movie[2]

        answer = dict(sorted(budgets.items(), key = lambda item: item[1], reverse=True)[:n])
        return answer
        
    def most_profitable(self, n):
        """
Метод возвращает dict с топовыми фильмами, где ключами являются названия фильмов, а
значениями - разница между совокупным мировым кассовым сбором и бюджетом.
Отсортируйте его по убыванию разницы.
        """
        profits = {}
        for movie in self.imdb_info:
            movie_name = self.movies_data[movie[0]]['title']
            if (movie[2] is not None) and (movie[3] is not None):
                profits[movie_name] = movie[3] - movie[2]
        
        profits = dict(sorted(profits.items(), key = lambda item: item[1], reverse=True)[:n])
        return profits
        
    def longest(self, n):
        """
Метод возвращает dict с топовыми фильмами, где ключами являются названия фильмов, а
значениями - время их выполнения. Если существует более одной версии – выберите любую.
Отсортируйте ее по времени выполнения в порядке убывания.
        """
        runtimes = {}
        for movie in self.imdb_info:
            movie_name = self.movies_data[movie[0]]['title']
            runtimes[movie_name] = int(movie[4].total_seconds()) // 60 #время в минутах

        runtimes = dict(sorted(runtimes.items(), key = lambda item: item[1], reverse=True)[:n])
        return runtimes
        
    def top_cost_per_minute(self, n):
        """
Метод возвращает dict с топовыми фильмами, где ключами являются названия фильмов, а
значениями - бюджеты, разделенные на время их выполнения. Бюджеты могут быть в разных валютах – не обращайте на это внимания. 
Значения должны быть округлены до 2 знаков после запятой. Отсортируйте его по убыванию деления.
        """
        costs = {}
        for movie in self.imdb_info:
            movie_name = self.movies_data[movie[0]]['title']
            if movie[2] is not None:
                cost_per_minute = round(movie[2] / (int(movie[4].total_seconds()) // 60), 2)
                costs[movie_name] = cost_per_minute

        costs = dict(sorted(costs.items(), key = lambda item: item[1], reverse=True)[:n])
        return costs
    
    def most_successful_directors(self, n):
        """
    Возвращает dict с топ-n режиссёрами по суммарной прибыли (Gross - Budget) их фильмов.
    Сортировка по убыванию прибыли.
        """
        director_profits = {}

        for movie in self.imdb_info:
            director = movie[1]
            budget = movie[2]
            gross = movie[3]
            if budget is not None and gross is not None:
                profit = gross - budget
                director_profits[director] = director_profits.get(director, 0) + profit

        top_directors = dict(sorted(director_profits.items(), key=lambda item: item[1], reverse=True)[:n])
        return top_directors
    
    def average_runtime_by_genre(self, n):
        """
        Возвращает dict из топ-n жанров по средней продолжительности фильмов (в минутах).
        Сортировка по убыванию средней продолжительности.
        """
        from collections import defaultdict

        genre_times = defaultdict(list)

        for movie in self.imdb_info:
            movie_id = movie[0]
            runtime = movie[4]
            if runtime is not None:
                genres = self.movies_data[movie_id]['genres'].split('|')
                for genre in genres:
                    genre_times[genre].append(int(runtime.total_seconds()) // 60)

        genre_avg = {
            genre: round(sum(times) / len(times), 2)
            for genre, times in genre_times.items() if len(times) > 0
        }

        sorted_genre_avg = dict(sorted(genre_avg.items(), key=lambda item: item[1], reverse=True)[:n])
        return sorted_genre_avg



class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.file_movies = path_to_the_file
        self.is_header = True
        self.movies = self.read_csv_movies()

    def parsing_by_str(self, line):
        """Парсит строку CSV с строгими проверками структуры"""
        answer = [""] * 3
        in_quotes = False
        index = 0
        
        for char in line:
            if char == '\"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                if index >= 2:
                    raise ValueError("Too many columns in CSV line")
                index += 1
            else:
                answer[index] += char
        
        if index < 2:
            raise ValueError("Not enough columns in CSV line")
        
        return answer

    def read_csv_movies(self):
        """Читает файл movies.csv со строгими проверками"""
        result = []
        max_lines = 1000
        
        def validate_header(file_obj, expected):
            header = file_obj.readline().strip()
            if header != expected:
                raise ValueError(f"Expected: '{expected}', got: '{header}'")

        with open(self.file_movies, 'r', encoding='utf-8') as f:
            if self.is_header:
                try:
                    validate_header(f, "movieId,title,genres")
                except ValueError as e:
                    raise ValueError(f"Invalid movies.csv header: {str(e)}")

            for line_num, line in enumerate(f, 1):
                if line_num > max_lines:
                    break

                try:
                    parts = self.parsing_by_str(line)
                except Exception as e:
                    raise ValueError(f"movies.csv line {line_num}: parsing error - {str(e)}")

                if len(parts) != 3:
                    raise ValueError(f"movies.csv line {line_num}: expected exactly 3 columns, got {len(parts)}")

                try:
                    movie_id = int(parts[0])
                    if movie_id <= 0:
                        raise ValueError("movieId must be positive integer")
                except ValueError:
                    raise ValueError(f"movies.csv line {line_num}: invalid movieId format (must be integer)")

                title = parts[1].strip()
                if not title:
                    raise ValueError(f"movies.csv line {line_num}: title cannot be empty")
                
                # Проверка года в названии
                if '(' not in title or ')' not in title:
                    raise ValueError(f"movies.csv line {line_num}: title must contain year in parentheses")

                genres = parts[2].strip()
                if not genres:
                    genres = "(no genres listed)"

                result.append({
                    'movieId': movie_id,
                    'title': title,
                    'genres': genres
                })
        
        return result

    def dist_by_release(self):
        """
Метод возвращает dict или OrderedDict, где ключами являются годы, а значениями - количество. 
Вам нужно извлечь годы из заголовков. Отсортируйте их по количеству в порядке убывания.
        """
        counts_by_year = {}
        for row in self.movies:
            year = self.take_year_from_title(row['title'])
            if year is not None:
                counts_by_year[year] = counts_by_year.get(year, 0) + 1
        
        return dict(sorted(counts_by_year.items(),key = lambda item: item[1], reverse=True))
    
    def take_year_from_title(self, title):
        is_bracket = 0
        count_of_numbers = 0
        reverse_year = ""
        for i in range(1,len(title)):
            if is_bracket == 2:
                break
            if (title[-i] in "()"):
                is_bracket += 1
                continue
            if is_bracket == 1:
                reverse_year += title[-i]
                count_of_numbers += 1
            if count_of_numbers == 4:
                break
        year = reverse_year[::-1]
        if year == '':
            return None
        return int(year)
            

    def dist_by_genres(self):
        """
Метод возвращает dict, где ключами являются жанры, а значениями - количество.
Отсортируйте его по количеству в порядке убывания.
        """ 
        counts_by_genres = {}
        for row in self.movies:
            list_of_genres = row['genres'].strip().split('|')
            for genre in list_of_genres:
                counts_by_genres[genre] = counts_by_genres.get(genre, 0) + 1

        genres = dict(sorted(counts_by_genres.items(), key = lambda item: item[1], reverse=True))
        return genres
        
    def most_genres(self, n):
        """
Метод возвращает dict, содержащий список из топ-n  фильмов, где ключами являются названия фильмов, а
значениями - количество жанров фильма. Отсортируйте его по убыванию номеров.
        """
        count_of_genres_by_movie = {}
        for row in self.movies:
            count_of_genres_by_movie[row['title']] = len(row['genres'].split('|'))
        
        movies = dict(sorted(count_of_genres_by_movie.items(), key = lambda item: item[1], reverse=True)[:n])
        
        return movies
    
    def dist_by_genre_combination(self):
        """
        Возвращает словарь, где ключ — это уникальная комбинация жанров (например, 'Action|Adventure'),
        а значение — количество фильмов с такой комбинацией.
        Результат отсортирован по убыванию количества.
        """
        combination_counts = {}
        for row in self.movies:
            combination = row['genres'].strip()
            combination_counts[combination] = combination_counts.get(combination, 0) + 1

        return dict(sorted(combination_counts.items(), key=lambda item: item[1], reverse=True))
    