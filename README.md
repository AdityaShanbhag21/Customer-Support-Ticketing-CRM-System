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

## Local Setup (Windows 11)

### 1. Clone / download the project

```powershell
cd C:\Projects
git clone <your-repo-url> datastraw-crm
cd datastraw-crm
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If you get a script execution policy error, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the API server

```powershell
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`  
Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

### 5. Open the frontend

Simply open `index.html` in your browser:

```powershell
start index.html
```

> The frontend calls `http://127.0.0.1:8000` by default. If you deploy the API to a different URL, update the `API` constant at the top of the `<script>` block in `index.html`.

---

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

## Deployment (Railway.app)

1. Push your code to GitHub (make sure `crm.db` and `venv/` are in `.gitignore`)
2. Create a new project on [Railway.app](https://railway.app) → **Deploy from GitHub repo**
3. Set the **Start Command** to: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Railway auto-detects Python and installs `requirements.txt`
5. Once deployed, copy the public URL and update the `API` constant in `index.html`
6. You can serve `index.html` as a static file — add this to `main.py`:

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def root():
    return FileResponse("index.html")
```

---

## Tech Choices

- **FastAPI** — modern, fast, async-ready Python API framework with auto-generated OpenAPI docs
- **SQLAlchemy 2.0** — battle-tested ORM; easy to swap SQLite for PostgreSQL in production
- **SQLite** — zero-config, file-based database; perfect for MVP and assessment purposes
- **Pydantic v2** — strict data validation with helpful error messages out of the box
- **Tailwind CSS (CDN)** — utility-first CSS with no build step required for a single-page frontend
- **Vanilla JS** — no framework overhead; keeps the frontend dependency-free and fast

---

## What I Would Add With More Time

- JWT authentication (login/logout, role-based access)
- Priority levels (Low / Medium / High / Critical) on tickets
- Email notifications when a ticket is created or updated
- Pagination for the ticket list
- Assigned agent per ticket with a team members table
- Dashboard analytics (tickets over time, resolution rate, average response time)
- Swap SQLite → PostgreSQL for production multi-user concurrency
"# Customer-Support-Ticketing-CRM-System" 
