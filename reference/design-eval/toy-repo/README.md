# Toy Item API

A tiny FastAPI service. All endpoints are authenticated via a JWT bearer token (`app/auth.py`).
Storage is in-memory (`app/db.py`) — a placeholder for a real database.

Endpoints live in `app/main.py`: list/create/get items, scoped to the authenticated user.
