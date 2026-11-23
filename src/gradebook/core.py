"""Simple student gradebook utilities (FINAL version - quality issues fixed)."""
import json
import os

NOT_AVAILABLE = "Not available"
GRADE_BANDS = ((90, "A"), (80, "B"), (70, "C"), (60, "D"))


def get_admin_password():
    """Read the admin password from the environment instead of hard-coding it."""
    return os.environ.get("GRADEBOOK_ADMIN_PASSWORD", "")


def calculate_average(scores):
    """Return the mean of a list of numeric scores (0 for an empty list)."""
    if not scores:
        return 0
    for score in scores:
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise TypeError(f"score must be a number, got {score!r}")
        if score < 0 or score > 100:
            raise ValueError(f"score must be between 0 and 100, got {score}")
    return sum(scores) / len(scores)


def letter_grade(score):
    """Convert a numeric score to a letter grade."""
    for minimum, letter in GRADE_BANDS:
        if score >= minimum:
            return letter
    return "F"


def load_students(path):
    """Load a list of students from a JSON file; return [] if missing or invalid."""
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _format_student(student, include_details, format_type):
    name = student.get("name")
    if name is None:
        return f"Unknown student | {NOT_AVAILABLE}"
    scores = student.get("scores")
    if not scores:
        return f"Student: {name} | {NOT_AVAILABLE}"
    if not include_details:
        return name
    avg = calculate_average(scores)
    grade = letter_grade(avg)
    if format_type == "long":
        return f"Student: {name} | Average: {round(avg, 1)} | Grade: {grade}"
    return f"{name} {grade}"


def build_report(students, include_details, format_type):
    """Build a multi-line text report for a list of students."""
    return "\n".join(_format_student(s, include_details, format_type) for s in students)
