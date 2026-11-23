import json

import pytest

from gradebook.core import (
    build_report,
    calculate_average,
    get_admin_password,
    letter_grade,
    load_students,
)


# ---------- Happy path: valid input gives the expected result ----------

def test_average_normal_scores():
    assert calculate_average([80, 90, 100]) == 90


def test_average_empty_list():
    assert calculate_average([]) == 0


@pytest.mark.parametrize(
    "score, expected",
    [(95, "A"), (90, "A"), (85, "B"), (75, "C"), (65, "D"), (40, "F")],
)
def test_letter_grades(score, expected):
    assert letter_grade(score) == expected


def test_load_students_valid_file(tmp_path):
    path = tmp_path / "students.json"
    path.write_text(json.dumps([{"name": "Ana", "scores": [90]}]), encoding="utf-8")
    assert load_students(path) == [{"name": "Ana", "scores": [90]}]


def test_report_long_format():
    report = build_report([{"name": "Ana", "scores": [90, 100]}], True, "long")
    assert report == "Student: Ana | Average: 95.0 | Grade: A"


def test_report_short_format():
    assert build_report([{"name": "Ben", "scores": [72]}], True, "short") == "Ben C"


def test_report_names_only():
    assert build_report([{"name": "Ana", "scores": [90]}], False, "long") == "Ana"


def test_admin_password_from_environment(monkeypatch):
    monkeypatch.setenv("GRADEBOOK_ADMIN_PASSWORD", "from-env")
    assert get_admin_password() == "from-env"


# ---------- Sad path: bad input is handled safely ----------

def test_average_rejects_negative_score():
    with pytest.raises(ValueError):
        calculate_average([90, -5])


def test_average_rejects_score_over_100():
    with pytest.raises(ValueError):
        calculate_average([101])


def test_average_rejects_text():
    with pytest.raises(TypeError):
        calculate_average([90, "eighty"])


def test_load_students_missing_file(tmp_path):
    assert load_students(tmp_path / "nope.json") == []


def test_load_students_corrupt_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    assert load_students(path) == []


def test_report_missing_fields():
    report = build_report([{"scores": [90]}, {"name": "Cy"}, {"name": "Di", "scores": []}], True, "long")
    assert report.splitlines() == [
        "Unknown student | Not available",
        "Student: Cy | Not available",
        "Student: Di | Not available",
    ]


def test_admin_password_missing(monkeypatch):
    monkeypatch.delenv("GRADEBOOK_ADMIN_PASSWORD", raising=False)
    assert get_admin_password() == ""
