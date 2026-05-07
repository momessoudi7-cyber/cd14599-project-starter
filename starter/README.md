# Udatracker Starter Code

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

## Project Reflection

This project was developed using Test-Driven Development (TDD) to solve the order management API problem. Writing tests first helped define the API contract clearly and kept each implementation step focused and verifiable.

The error handling design is intentionally consistent: every failure returns structured JSON like `{"error": "..."}` with an appropriate HTTP status code. This makes client behavior predictable and simplifies validation of invalid input, missing resources, and update failures.

## Recommended Next Steps

- Add a persistent database backend (SQLite or PostgreSQL) and replace the in-memory storage layer.
- Introduce request schema validation with a library such as Marshmallow or Pydantic.
- Add authentication and authorization to protect order operations.
- Implement pagination and richer filtering for `GET /api/orders`.
- Add OpenAPI/Swagger documentation for the public API.
- Improve frontend integration so the UI consumes the API directly and displays error messages clearly.

