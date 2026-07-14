import pytest
import os
import datetime
from src.movielens_analysis import Links

# Пути к валидным и невалидным данным
@pytest.fixture(scope="module")
def valid_links_path():
    return os.path.abspath("./mock_data_file_for_test/links_validate/links.csv")

@pytest.fixture(scope="module")
def invalid_links_path():
    return os.path.abspath("./mock_data_file_for_test/links_not_validate/links.csv")

@pytest.fixture(scope="module")
def valid_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_validate/movies.csv")

@pytest.fixture(scope="module")
def invalid_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_not_validate/movies.csv")


# Тесты на ошибки
def test_invalid_links_raises_exception(invalid_links_path, valid_movies_path):
    with pytest.raises(Exception):
        Links(invalid_links_path, valid_movies_path)

def test_invalid_movies_raises_exception(valid_links_path, invalid_movies_path):
    with pytest.raises(Exception):
        Links(valid_links_path, invalid_movies_path)

def test_nonexistent_links_file_raises_exception(valid_movies_path):
    with pytest.raises(Exception):
        Links("./no_such_file.csv", valid_movies_path)

def test_nonexistent_movies_file_raises_exception(valid_links_path):
    with pytest.raises(Exception):
        Links(valid_links_path, "./no_such_file.csv")


# Тест на успешную загрузку валидных данных
def test_valid_data_loads_successfully(valid_links_path, valid_movies_path):
    links = Links(valid_links_path, valid_movies_path)
    assert isinstance(links.movies_data, dict)
    assert all(isinstance(mid, int) for mid in links.movies_data.keys())


# Тест get_imdb с реальными запросами
def test_get_imdb_real_request(valid_links_path, valid_movies_path):
    links = Links(valid_links_path, valid_movies_path)
    result = links.get_imdb([1, 2], ['Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime'])
    
    assert isinstance(result, list)
    assert all(isinstance(row, list) for row in result)
    assert all(len(row) == 5 for row in result)

    for row in result:
        movie_id, director, budget, gross, runtime = row
        assert isinstance(movie_id, int)
        assert isinstance(director, str)
        assert isinstance(budget, int)
        assert isinstance(gross, int)
        assert isinstance(runtime, datetime.timedelta)


# Тесты на сортировку и типы возвращаемых значений
@pytest.fixture(scope="module")
def imdb_info_fixture(valid_links_path, valid_movies_path):
    links = Links(valid_links_path, valid_movies_path)
    result = links.get_imdb([1, 2, 3], ['Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime'])

    # Проверка на соответствие ожидаемым данным, чтобы убедиться, что всё правильно загрузилось
    expected = [
        [3, 'Howard Deutch', 25000000, 71518503, datetime.timedelta(seconds=6060)],
        [2, 'Joe Johnston', 65000000, 262821940, datetime.timedelta(seconds=6240)],
        [1, 'John Lasseter', 30000000, 394436586, datetime.timedelta(seconds=4860)]
    ]
    assert result == expected
    return links


def test_top_directors_return_type(imdb_info_fixture):
    result = imdb_info_fixture.top_directors(1)
    assert isinstance(result, dict)
    assert all(isinstance(k, str) and isinstance(v, int) for k, v in result.items())

def test_most_expensive_sorted(imdb_info_fixture):
    result = imdb_info_fixture.most_expensive(2)
    budgets = list(result.values())
    assert all(budgets[i] >= budgets[i+1] for i in range(len(budgets)-1))

def test_most_profitable_sorted(imdb_info_fixture):
    result = imdb_info_fixture.most_profitable(2)
    profits = list(result.values())
    assert all(profits[i] >= profits[i+1] for i in range(len(profits)-1))

def test_longest_sorted(imdb_info_fixture):
    result = imdb_info_fixture.longest(2)
    durations = list(result.values())
    assert all(durations[i] >= durations[i+1] for i in range(len(durations)-1))

def test_top_cost_per_minute_sorted_and_rounded(imdb_info_fixture):
    result = imdb_info_fixture.top_cost_per_minute(2)
    costs = list(result.values())
    assert all(isinstance(cost, float) for cost in costs)
    assert all(round(cost, 2) == cost for cost in costs)
    assert all(costs[i] >= costs[i+1] for i in range(len(costs)-1))

def test_top_genres_by_budget_return_type(imdb_info_fixture):
    result = imdb_info_fixture.average_runtime_by_genre(3)
    assert isinstance(result, dict)
    assert all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in result.items())

def test_top_genres_by_budget_sorted(imdb_info_fixture):
    result = imdb_info_fixture.average_runtime_by_genre(3)
    budgets = list(result.values())
    assert all(budgets[i] >= budgets[i+1] for i in range(len(budgets)-1))

def test_director_success_ratio_return_type(imdb_info_fixture):
    result = imdb_info_fixture.most_successful_directors(2)
    assert isinstance(result, dict)
    assert all(isinstance(k, str) and isinstance(v, int) for k, v in result.items())

def test_director_success_ratio_sorted(imdb_info_fixture):
    result = imdb_info_fixture.most_successful_directors(2)
    ratios = list(result.values())
    assert all(ratios[i] >= ratios[i+1] for i in range(len(ratios)-1))

def test_top_directors_exact_value(imdb_info_fixture):
    result = imdb_info_fixture.top_directors(1)
    assert result == {'Howard Deutch': 1}

def test_most_expensive_exact_value(imdb_info_fixture):
    result = imdb_info_fixture.most_expensive(1)
    assert result == {'Jumanji (1995)': 65000000}

def test_most_profitable_exact_value(imdb_info_fixture):
    result = imdb_info_fixture.most_profitable(1)
    assert result == {'Toy Story (1995)': 364436586}

def test_longest_exact_value(imdb_info_fixture):
    result = imdb_info_fixture.longest(1)
    assert result == {'Jumanji (1995)': 104}

def test_top_cost_per_minute_exact_value(imdb_info_fixture):
    result = imdb_info_fixture.top_cost_per_minute(1)
    assert result == {'Jumanji (1995)': 625000.0}

def test_average_runtime_by_genre_exact_value(imdb_info_fixture):
    result = imdb_info_fixture.average_runtime_by_genre(1)
    assert result == {'Romance': 101.0}

