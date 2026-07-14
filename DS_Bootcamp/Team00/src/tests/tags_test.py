import datetime

import pytest
from src.movielens_analysis import Tags
import os


@pytest.fixture
def valid_path():
    return os.path.abspath("./mock_data_file_for_test/tags_validate/tags.csv")

def test_with_valid_files(valid_path):
    tags = Tags(valid_path)
    assert tags is not None
    assert len(tags.tags_csv) > 0


def test_data_content(valid_path):
    ratings = Tags(valid_path)

    for tag in ratings.tags_csv:
        assert 'userId' in tag
        assert 'movieId' in tag
        assert 'tag' in tag
        assert 'timestamp' in tag

        assert isinstance(tag['userId'], int)
        assert isinstance(tag['movieId'], int)
        assert isinstance(tag['tag'], str)
        assert isinstance(tag['timestamp'], datetime.datetime)

def test_most_words(valid_path):
    assert Tags(valid_path).most_words(3) == {'way too long': 3, 'indie record label': 3, 'magic board game': 3}

def test_most_words_type(valid_path):
    assert isinstance(Tags(valid_path).most_words(3), dict)

def test_longest(valid_path):
    assert Tags(valid_path).longest(3) == ['Oscar (Best Cinematography)', 'Leonardo DiCaprio', 'indie record label']

def test_longest_type(valid_path):
    assert isinstance(Tags(valid_path).longest(3), list)

def test_most_words_and_longest(valid_path):
    assert Tags(valid_path).most_words_and_longest(3) == ['indie record label']

def test_most_words_and_longest_type(valid_path):
    assert isinstance(Tags(valid_path).most_words_and_longest(3), list)

def test_most_popular(valid_path):
    assert Tags(valid_path).most_popular(3) == {'Al Pacino': 2, 'twist ending': 2, 'funny': 1}

def test_most_popular_type(valid_path):
    assert isinstance(Tags(valid_path).most_popular(3), dict)

def test_tags_with(valid_path):
    assert Tags(valid_path).tags_with('Tom') == ['Tom Hardy']

def test_tags_with_type(valid_path):
    assert isinstance(Tags(valid_path).tags_with('Tom'), list)

def test_tags_starting_with_letter(valid_path):
    assert Tags(valid_path).tags_starting_with_letter('Chri') == ['Christina Ricci', 'Christopher Lloyd']

def test_tags_starting_with_letter_type(valid_path):
    assert isinstance(Tags(valid_path).tags_starting_with_letter('Chri'), list)