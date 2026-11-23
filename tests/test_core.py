from gradebook.core import calculate_average, letter_grade


def test_average_normal_scores():
    assert calculate_average([80, 90, 100]) == 90


def test_average_empty_list():
    assert calculate_average([]) == 0


def test_letter_grade_a():
    assert letter_grade(95) == "A"


def test_letter_grade_f():
    assert letter_grade(40) == "F"
