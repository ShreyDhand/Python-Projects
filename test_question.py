import re
from unittest.mock import patch

import pytest

from question import Question


@pytest.fixture
def question():
    """Fixture with set question and answers"""
    q = Question(
        "Question text",
        "correct",
        ["wrong", "false", "incorrect"],
        "category",
        "medium",
    )
    q.answers = ["correct", "wrong", "false", "incorrect"]
    q.answer_id = 1
    return q


def test_question():
    """Simple attribute check"""
    question = Question(
        "Question text",
        "correct",
        ["wrong", "false", "incorrect"],
        "category",
        "medium",
    )
    assert question.question == "Question text"
    assert "correct" in question.answers
    assert "incorrect" in question.answers
    assert question.difficulty == "medium"
    assert question.category == "category"


def test_string(question):
    """Tests the str method"""
    question_string = str(question)
    lines = question_string.split("\n")
    assert "Question text" in question_string
    assert re.search(r"1\W+correct", question_string)
    assert "correct" in lines[1]

    assert lines[4].startswith("4")
    assert "incorrect" in lines[4]


@patch("random.shuffle")
def test_random_question(mock_random):
    """Checks the constructor calls random.shuffle at least once"""
    q = Question(
        "Question?", "correct", ["wrong", "incorrect", "false"], "general", "medium"
    )
    assert mock_random.call_count >= 1


def test_difficulty():
    """Checks the constructor raises an exception when an invalid difficulty is provided"""
    with pytest.raises(AttributeError):
        q = Question(
            "Question?",
            "correct",
            ["wrong", "incorrect", "false"],
            "general",
            "whatever",
        )

    for difficulty in ("easy", "medium", "hard"):
        q = Question(
            "Question?",
            "correct",
            ["wrong", "incorrect", "false"],
            "general",
            difficulty,
        )
        assert q.difficulty == difficulty
