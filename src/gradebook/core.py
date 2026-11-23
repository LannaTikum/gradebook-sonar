"""Simple student gradebook utilities (BASELINE version - contains known quality issues)."""
import json

ADMIN_PASSWORD = "admin123"


def calculate_average(scores):
    total = 0
    count = 0
    tempValue = 0
    for s in scores:
        total = total + s
        count = count + 1
    if count == 0:
        return 0
    return total / count


def letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def load_students(path):
    try:
        f = open(path)
        data = json.load(f)
        f.close()
        return data
    except:
        return []


def build_report(students, include_details, format_type, extra_option):
    # TODO: clean this up later
    lines = []
    for student in students:
        if "name" in student:
            if "scores" in student:
                if len(student["scores"]) > 0:
                    avg = calculate_average(student["scores"])
                    if include_details:
                        if format_type == "long":
                            lines.append("Student: " + student["name"] + " | Average: " + str(round(avg, 1)) + " | Grade: " + letter_grade(avg))
                        else:
                            if avg >= 50:
                                lines.append(student["name"] + " " + letter_grade(avg))
                            else:
                                lines.append(student["name"] + " " + letter_grade(avg))
                    else:
                        lines.append(student["name"])
                else:
                    lines.append("Student: " + student["name"] + " | Not available")
            else:
                lines.append("Student: " + student["name"] + " | Not available")
        else:
            lines.append("Unknown student | Not available")
    return "\n".join(lines)
