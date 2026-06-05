"""
main.py
-------
FastAPI application entry point.

Endpoints:
    POST   /api/tickets              — Create a new support ticket
    GET    /api/tickets              — List tickets (optional filter & search)
    GET    /api/tickets/{ticket_id}  — Get full details of one ticket
    PUT    /api/tickets/{ticket_id}  — Update status and/or add a note
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# ---------------------------------------------------------------------------
# Bootstrap — create all tables if they don't exist yet
# ---------------------------------------------------------------------------
models.Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Datastraw Support CRM",
    description="Customer support ticketing system built with FastAPI + SQLite.",
    version="1.0.0",
)

# Allow the HTML frontend (served on any origin during development) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper — generate the next ticket ID
# ---------------------------------------------------------------------------

def _generate_ticket_id(db: Session) -> str:
    """
    Returns the next sequential ticket ID in the format TKT-XXX.
    Reads the highest existing numeric suffix and increments it.
    """
    last_ticket = (
        db.query(models.Ticket)
        .order_by(models.Ticket.id.desc())
        .first()
    )
    if last_ticket is None:
        next_num = 1
    else:
        # ticket_id format: "TKT-001"
        try:
            next_num = int(last_ticket.ticket_id.split("-")[1]) + 1
        except (IndexError, ValueError):
            next_num = last_ticket.id + 1

    return f"TKT-{next_num:03d}"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.post(
    "/api/tickets",
    response_model=schemas.TicketCreateResponse,
    status_code=201,
    summary="Create a new support ticket",
)
def create_ticket(
    payload: schemas.TicketCreate,
    db: Session = Depends(get_db),
):
    """
    Accepts customer details and issue information, generates a unique
    ticket ID, persists the record, and returns the new ticket ID and
    creation timestamp.
    """
    ticket_id = _generate_ticket_id(db)

    now = datetime.now(timezone.utc)
    new_ticket = models.Ticket(
        ticket_id=ticket_id,
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        subject=payload.subject,
        description=payload.description,
        status="Open",
        created_at=now,
        updated_at=now,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@app.get(
    "/api/tickets",
    response_model=list[schemas.TicketSummary],
    summary="List all tickets with optional filter and search",
)
def list_tickets(
    status: Optional[str] = Query(None, description="Filter by status: Open | In Progress | Closed"),
    search: Optional[str] = Query(None, description="Search by customer name, email, or subject"),
    db: Session = Depends(get_db),
):
    """
    Returns a list of tickets ordered by creation date (newest first).
    Supports optional filtering by status and a full-text search across
    customer_name, customer_email, and subject fields.
    """
    query = db.query(models.Ticket)

    if status:
        query = query.filter(models.Ticket.status == status)

    if search:
        like_expr = f"%{search}%"
        query = query.filter(
            models.Ticket.customer_name.ilike(like_expr)
            | models.Ticket.customer_email.ilike(like_expr)
            | models.Ticket.subject.ilike(like_expr)
            | models.Ticket.description.ilike(like_expr)
            | models.Ticket.ticket_id.ilike(like_expr)
        )

    return query.order_by(models.Ticket.created_at.desc()).all()


@app.get(
    "/api/tickets/{ticket_id}",
    response_model=schemas.TicketDetail,
    summary="Get full details of a single ticket",
)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
):
    """
    Returns all fields for the requested ticket, including all associated
    notes sorted by creation time (oldest first).
    """
    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.ticket_id == ticket_id)
        .first()
    )
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found.")
    return ticket


@app.put(
    "/api/tickets/{ticket_id}",
    response_model=schemas.TicketUpdateResponse,
    summary="Update ticket status and optionally add a note",
)
def update_ticket(
    ticket_id: str,
    payload: schemas.TicketUpdate,
    db: Session = Depends(get_db),
):
    """
    Updates the ticket's status if provided, and appends a new note to
    the notes table if note text is supplied.  Returns success flag and
    the updated_at timestamp.
    """
    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.ticket_id == ticket_id)
        .first()
    )
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found.")

    now = datetime.now(timezone.utc)

    if payload.status is not None:
        ticket.status = payload.status.value
        ticket.updated_at = now

    if payload.note:
        new_note = models.Note(
            ticket_id=ticket_id,
            note_text=payload.note,
            created_at=now,
        )
        db.add(new_note)
        ticket.updated_at = now  # bump updated_at whenever a note is added

    db.commit()
    db.refresh(ticket)

    return schemas.TicketUpdateResponse(success=True, updated_at=ticket.updated_at)
