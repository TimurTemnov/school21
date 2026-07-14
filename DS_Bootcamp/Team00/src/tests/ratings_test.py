import datetime

import pytest
from src.movielens_analysis import Ratings
import os


@pytest.fixture
def valid_ratings_path():
    return os.path.abspath("./mock_data_file_for_test/ratings_validate/ratings.csv")


@pytest.fixture
def invalid_ratings_path():
    return os.path.abspath("./mock_data_file_for_test/ratings_validate/ratings123.csv")


@pytest.fixture
def invalid_data_ratings_path():
    return os.path.abspath("./mock_data_file_for_test/ratings_validate/ratings.csv")


@pytest.fixture
def valid_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_validate/movies.csv")


@pytest.fixture
def invalid_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_validate/movies123.csv")


@pytest.fixture
def invalid_data_movies_path():
    return os.path.abspath("./mock_data_file_for_test/movies_validate/movies.csv")


def test_with_valid_files(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    assert ratings is not None
    assert len(ratings.ratings) > 0
    assert len(ratings.movies) > 0


def test_with_invalid_path_ratings(invalid_ratings_path, valid_movies_path):
    with pytest.raises(FileNotFoundError) as excinfo:
        Ratings(invalid_ratings_path, valid_movies_path)
    assert "не существует" in str(excinfo.value).lower()


def test_with_invalid_path_movies(valid_ratings_path, invalid_movies_path):
    with pytest.raises((ValueError, FileNotFoundError)) as excinfo:
        Ratings(valid_ratings_path, invalid_movies_path)
    assert "не существует" in str(excinfo.value).lower()


def test_with_both_invalid_path_files(invalid_ratings_path, invalid_movies_path):
    with pytest.raises((ValueError, FileNotFoundError)) as excinfo:
        Ratings(invalid_ratings_path, invalid_movies_path)
    assert ("ratings" in str(excinfo.value).lower() or
            ("movies" in str(excinfo.value).lower()))


def test_ratings_data_content(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)

    for rating in ratings.ratings:
        assert 'userId' in rating
        assert 'movieId' in rating
        assert 'rating' in rating
        assert 'timestamp' in rating

        assert isinstance(rating['userId'], int)
        assert isinstance(rating['movieId'], int)
        assert isinstance(rating['rating'], float)
        assert isinstance(rating['timestamp'], datetime.datetime)


def test_movies_data_content(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)

    for movie in ratings.movies:
        assert 'movieId' in movie
        assert 'title' in movie
        assert 'genres' in movie

        assert isinstance(movie['movieId'], int)
        assert isinstance(movie['title'], str)
        assert isinstance(movie['genres'], str)


def test_file_existence_validation():
    with pytest.raises(FileNotFoundError):
        Ratings("nonexistent_ratings.csv", "nonexistent_movies.csv")


def test_file_format_validation(tmp_path):
    invalid_file = tmp_path / "wrong_format.txt"
    invalid_file.write_text("This is not a CSV file")

    with pytest.raises(FileNotFoundError):
        Ratings(str(invalid_file), "movies_validate.csv")

def test_dist_by_year_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.dist_by_year()
    assert result == {2000: 49}

def test_dist_by_rating_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.dist_by_rating()
    assert result == {3.0: 10, 4.0: 18, 5.0: 21}

def test_top_by_num_of_ratings_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_by_num_of_ratings(5)
    assert result == {'Toy Story (1995)': 1, 'Grumpier Old Men (1995)': 1, 'Heat (1995)': 1, 'Seven (a.k.a. Se7en) (1995)': 1, '"Usual Suspects': 1}


def test_top_by_ratings_median_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_by_ratings(2, metric='median')
    assert result == {'Seven (a.k.a. Se7en) (1995)': 5.0, '"Usual Suspects': 5.0}

def test_top_by_ratings_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_by_ratings(2)
    assert result == {'Seven (a.k.a. Se7en) (1995)': 5.0, '"Usual Suspects': 5.0}

def test_top_controversial_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_controversial(3)
    assert result == {'Toy Story (1995)': 0.0, 'Grumpier Old Men (1995)': 0.0, 'Heat (1995)': 0.0}

def test_user_dist_by_rating_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Users(ratings.ratings)
    result = movies.dist_by_rating()
    assert result == {1: 49}

def test_user_top_by_rating_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Users(ratings.ratings)
    result = movies.top_by_rating(metric='median')
    assert result == {1: 4.0}

def test_user_top_by_rating_median_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Users(ratings.ratings)
    result = movies.top_by_rating()
    assert result == {1: 4.22}

def test_user_top_controversial_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Users(ratings.ratings)
    result = movies.top_controversial(1)
    assert result == {1: 0.58}

def test_dist_by_year_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.dist_by_year()
    assert isinstance(result, dict)

def test_dist_by_rating_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.dist_by_rating()
    assert isinstance(result, dict)

def test_top_by_num_of_ratings_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_by_num_of_ratings(5)
    assert isinstance(result, dict)

def test_top_by_ratings_median_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_by_ratings(2, metric='median')
    assert isinstance(result, dict)

def test_top_by_ratings_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_by_ratings(2)
    assert isinstance(result, dict)

def test_top_controversial_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    result = movies.top_controversial(3)
    assert isinstance(result, dict)

def test_user_dist_by_rating_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    users = ratings.Users(ratings.ratings)
    result = users.dist_by_rating()
    assert isinstance(result, dict)

def test_user_top_by_rating_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    users = ratings.Users(ratings.ratings)
    result = users.top_by_rating(metric='median')
    assert isinstance(result, dict)

def test_user_top_by_rating_median_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    users = ratings.Users(ratings.ratings)
    result = users.top_by_rating()
    assert isinstance(result, dict)

def test_user_top_controversial_data_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    users = ratings.Users(ratings.ratings)
    result = users.top_controversial(1)
    assert isinstance(result, dict)

def test_users_top_by_rating_invalid_metric(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    users = ratings.Users(ratings.ratings)
    with pytest.raises(Exception):
        users.top_by_rating(metric='invalid')

def test_count_ratings_per_movie_data(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    assert movies.count_ratings_per_movie() == {'Toy Story (1995)': 1, 'Grumpier Old Men (1995)': 1, 'Heat (1995)': 1, 'Seven (a.k.a. Se7en) (1995)': 1, '"Usual Suspects': 1}

def test_count_ratings_per_movie_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    assert isinstance(movies.count_ratings_per_movie(), dict)

def test_count_unique_movies_by_genre_top_five(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    assert movies.count_unique_movies_by_genre_top_five() == {'Drama': 22, 'Comedy': 13, 'Romance': 11, 'Crime': 9, 'Thriller': 9}

def test_count_unique_movies_by_genre_top_five_type(valid_ratings_path, valid_movies_path):
    ratings = Ratings(valid_ratings_path, valid_movies_path)
    movies = ratings.Movies(ratings.ratings, ratings.movies)
    assert isinstance(movies.count_unique_movies_by_genre_top_five(), dict)