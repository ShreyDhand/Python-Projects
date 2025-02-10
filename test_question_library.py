import pytest
from unittest.mock import mock_open, patch


from question import Question
from question_library import QuestionLibrary

JSON_FILE = """[
    {
        "question": "MEDIUM question (general category)?",
        "correct_answer": "correct",
        "incorrect_answers": ["wrong", "false", "incorrect"],
        "category": "general",
        "difficulty": "medium"
    },
    {
        "difficulty": "hard",
        "category": "other",
        "question": "HARD question (other category)?",
        "incorrect_answers": ["wrong", "false", "incorrect"],
        "correct_answer": "correct"
    }
]"""


@pytest.fixture
@patch("builtins.open", new_callable=mock_open, read_data=JSON_FILE)
def lib(mock_file):
    return QuestionLibrary("somefile.json")


def test_library_init():
    with patch(
        "builtins.open", new_callable=mock_open, read_data=JSON_FILE
    ) as mock_file:
        lib = QuestionLibrary(
            "THAT_FILE_DOES_NOT_EXIST_BUT_ITS_OK_BECAUSE_I_USED_PATCH.whynot"
        )
        # Only should have been called once
        assert mock_file.call_count == 1
        # Assert open() used the file name provided in the constructor
        assert "THAT_FILE_DOES_NOT_EXIST_BUT_ITS_OK_BECAUSE_I_USED_PATCH.whynot" in mock_file.call_args.args


def test_library(lib):
    """Simple test and type checks"""
    assert len(lib) == 2
    assert all([type(q) == Question for q in lib.questions])


def test_library_random_get(lib):
    """Make sure we get random questions when pulling from the library"""
    with patch("random.shuffle") as mock_random:
        qs = lib.get_questions()
        assert mock_random.call_count == 1


def test_library_get(lib):
    """Make sure the get_questions filter the questions correctly"""
    qs = lib.get_questions(category="other")
    assert len(qs) == 1
    assert qs[0].category == "other"

    qs = lib.get_questions(difficulty="hard")
    assert len(qs) == 1
    assert qs[0].difficulty == "hard"

    # An invalid difficulty will be accepted, but no filtering will be done
    qs = lib.get_questions(difficulty="whatever")
    assert len(qs) == 2
    assert "hard" in [q.difficulty for q in lib.questions]
    assert "medium" in [q.difficulty for q in lib.questions]

    # Check the number argument works too
    qs = lib.get_questions(number=2)
    assert len(qs) == 2

    qs = lib.get_questions(number=1)
    assert len(qs) == 1

    qs = lib.get_questions(number=3)
    assert len(qs) == 2

    qs = lib.get_questions(category="other", number=2)
    assert len(qs) == 1

    qs = lib.get_questions(difficulty="whatever", number=1)
    assert len(qs) == 1


def test_get_categories(lib):
    """Checks the get_categories"""
    cats = lib.get_categories()
    assert len(cats) == 2
    assert "general" in cats
    assert "other" in cats
