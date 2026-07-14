import pytest
import os
from src.movielens_analysis import Movies

@pytest.fixture
def valid_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_validate/movies.csv")

@pytest.fixture
def invalid_data_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_not_validate/movies.csv")

# Тесты на исключения
def test_invalid_data_raises_exception(invalid_data_movies_path):
    """Проверяем что невалидные данные вызывают исключение"""
    with pytest.raises(Exception):
        Movies(invalid_data_movies_path)

def test_nonexistent_file_raises_exception():
    """Проверяем что несуществующий путь вызывает исключение"""
    with pytest.raises(Exception):
        Movies("./nonexistent/path/movies.csv")

# Тесты на валидные данные
def test_valid_data_no_exception(valid_movies_path):
    """Проверяем что валидные данные не вызывают исключение"""
    movies = Movies(valid_movies_path)
    assert movies is not None

def test_return_types(valid_movies_path):
    """Проверяем типы возвращаемых данных"""
    movies = Movies(valid_movies_path)
    
    assert isinstance(movies.dist_by_release(), dict)
    assert isinstance(movies.dist_by_genres(), dict)
    assert isinstance(movies.most_genres(5), dict)

def test_dist_by_release_sorted(valid_movies_path):
    """Проверяем правильность сортировки по годам"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_release()
    years = list(result.values())
    assert all(years[i] >= years[i+1] for i in range(len(years)-1))

def test_dist_by_genres_sorted(valid_movies_path):
    """Проверяем правильность сортировки по жанрам"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_genres()
    counts = list(result.values())
    assert all(counts[i] >= counts[i+1] for i in range(len(counts)-1))

def test_most_genres_sorted(valid_movies_path):
    """Проверяем правильность сортировки топ-n фильмов"""
    movies = Movies(valid_movies_path)
    result = movies.most_genres(5)
    counts = list(result.values())
    assert all(counts[i] >= counts[i+1] for i in range(len(counts)-1))

def test_most_genres_count(valid_movies_path):
    """Проверяем точное количество возвращаемых фильмов"""
    movies = Movies(valid_movies_path)
    assert len(movies.most_genres(3)) == 3
    assert len(movies.most_genres(0)) == 0

def test_dist_by_genre_combination_type(valid_movies_path):
    """Проверка, что метод возвращает словарь"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_genre_combination()
    assert isinstance(result, dict)

def test_dist_by_genre_combination_sorted(valid_movies_path):
    """Проверка, что значения отсортированы по убыванию"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_genre_combination()
    counts = list(result.values())
    assert all(counts[i] >= counts[i+1] for i in range(len(counts)-1))

def test_dist_by_release_values(valid_movies_path):
    """Проверяем точные значения по годам релиза"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_release()
    expected = {1995: 47}
    assert result == expected

def test_dist_by_genres_values(valid_movies_path):
    """Проверяем точные значения по жанрам"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_genres()
    expected_top3 = {
        'Drama': 25,
        'Comedy': 14,
        'Romance': 12
    }
    keys = list(result.keys())[:3]
    for i, genre in enumerate(expected_top3):
        assert genre == keys[i]
        assert result[genre] == expected_top3[genre]

def test_most_genres_values(valid_movies_path):
    """Проверяем топ фильмов с наибольшим числом жанров"""
    movies = Movies(valid_movies_path)
    result = movies.most_genres(3)
    expected = {
        'Toy Story (1995)': 5,
        'Money Train (1995)': 5,
        'Copycat (1995)': 5
    }
    assert list(result.items())[:3] == list(expected.items())

def test_dist_by_genre_combination_values(valid_movies_path):
    """Проверка первых значений для genre combination"""
    movies = Movies(valid_movies_path)
    result = movies.dist_by_genre_combination()
    expected_top3 = {
        'Drama': 5,
        'Drama|Romance': 5,
        'Comedy|Romance': 3
    }
    items = list(result.items())[:3]
    for (combo, count), (exp_combo, exp_count) in zip(items, expected_top3.items()):
        assert combo == exp_combo
        assert count == exp_count

