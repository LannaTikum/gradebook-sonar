# gradebook-sonar

A small Python library that averages student scores, converts them to letter
grades, loads student data from JSON, and builds a text report.

- Language: Python 3.12
- Test framework: pytest (+ pytest-cov for coverage)
- CI: GitHub Actions + SonarQube Cloud

Run locally:

    pip install -r requirements-dev.txt
    pytest --cov --cov-report=term
