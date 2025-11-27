# Task Analyzer - Sample Submission
This repository contains a minimal implementation for the **Smart Task Analyzer** assignment.
It includes:
- A simple Django-compatible backend layout (minimal, uses pure Django views and JSON)
- A scoring algorithm (`scoring.py`) with unit tests
- Frontend static files (`frontend/`) that call the API endpoints
- `requirements.txt` listing required packages

## Quick notes
- This is a simplified, local-ready implementation intended for an assignment demo.
- To run the Django app for full testing, install requirements and run `python manage.py runserver`.
- The scoring algorithm is in `backend/tasks/scoring.py`. Unit tests are in `backend/tasks/tests.py`.

## Files
See the `backend/` and `frontend/` directories for code.

## Algorithm summary (short)
The scoring function combines:
- Urgency score (based on days until due; overdue gets a strong boost)
- Importance (1-10)
- Effort (estimated_hours -> quick tasks get bonus)
- Dependency impact (tasks that block others get higher priority)
Scores are normalized to a 0-100 range.

