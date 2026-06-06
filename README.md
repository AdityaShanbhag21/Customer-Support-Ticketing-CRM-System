# Support CRM

A full-stack customer support ticketing system built with **FastAPI**, **SQLite**, and **Vanilla JS + Tailwind CSS**.

---

## Project Structure

```
support-crm/
├── venv/               ← Python virtual environment (not committed)
├── database.py         ← SQLAlchemy engine, session factory, get_db dependency
├── models.py           ← ORM table definitions (Ticket, Note)
├── schemas.py          ← Pydantic request/response models
├── main.py             ← FastAPI app, all 4 REST endpoints
├── index.html          ← Frontend (single file, no build step)
├── requirements.txt    ← Python dependencies
├── .env.example        ← Environment variable template
└── .gitignore
```

---

The API will be available at: `http://127.0.0.1:8000`  
Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`


## API Endpoints

| Method | Endpoint                        | Description                              |
|--------|---------------------------------|------------------------------------------|
| POST   | `/api/tickets`                  | Create a new support ticket              |
| GET    | `/api/tickets`                  | List all tickets (filter + search)       |
| GET    | `/api/tickets/{ticket_id}`      | Get full details + notes for one ticket  |
| PUT    | `/api/tickets/{ticket_id}`      | Update status and/or add a note          |

### Query parameters for `GET /api/tickets`

| Param    | Example                  | Description                                    |
|----------|--------------------------|------------------------------------------------|
| `status` | `?status=Open`           | Filter by Open, In Progress, or Closed         |
| `search` | `?search=Jane`           | Search across name, email, subject, description|

---

## Database Schema

### `tickets`

| Column          | Type         | Notes                        |
|-----------------|--------------|------------------------------|
| id              | INTEGER (PK) | Auto-increment               |
| ticket_id       | TEXT (UNIQUE)| e.g. TKT-001                 |
| customer_name   | TEXT         | Required                     |
| customer_email  | TEXT         | Required, validated as email |
| subject         | TEXT         | Required                     |
| description     | TEXT         | Required                     |
| status          | TEXT         | Open / In Progress / Closed  |
| created_at      | DATETIME     | UTC, auto-set                |
| updated_at      | DATETIME     | UTC, auto-updated            |

### `notes`

| Column    | Type         | Notes                          |
|-----------|--------------|--------------------------------|
| id        | INTEGER (PK) | Auto-increment                 |
| ticket_id | TEXT (FK)    | References tickets.ticket_id   |
| note_text | TEXT         | Required                       |
| created_at| DATETIME     | UTC, auto-set                  |

---
## Tech Choices

- **FastAPI** — modern, fast, async-ready Python API framework with auto-generated OpenAPI docs
- **SQLAlchemy 2.0** — battle-tested ORM; easy to swap SQLite for PostgreSQL in production
- **SQLite** — zero-config, file-based database; perfect for MVP and assessment purposes
- **Pydantic v2** — strict data validation with helpful error messages out of the box
- **Tailwind CSS (CDN)** — utility-first CSS with no build step required for a single-page frontend
- **Vanilla JS** — no framework overhead; keeps the frontend dependency-free and fast

---

