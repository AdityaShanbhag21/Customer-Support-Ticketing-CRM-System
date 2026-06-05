"""
schemas.py
----------
Pydantic models used for request body validation and API response serialization.
These are separate from the SQLAlchemy ORM models in models.py.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TicketStatus(str, Enum):
    """Valid status values for a ticket."""
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"


# ---------------------------------------------------------------------------
# Note schemas
# ---------------------------------------------------------------------------

class NoteBase(BaseModel):
    note_text: str = Field(..., min_length=1, description="Content of the note")


class NoteCreate(NoteBase):
    """Schema used when creating a note (internally by PUT /api/tickets/{id})."""
    pass


class NoteOut(NoteBase):
    """Schema returned when reading a note."""
    id: int
    ticket_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Ticket schemas
# ---------------------------------------------------------------------------

class TicketCreate(BaseModel):
    """
    Schema for POST /api/tickets request body.
    All fields are required when creating a new ticket.
    """
    customer_name: str = Field(..., min_length=1, max_length=150)
    customer_email: EmailStr
    subject: str = Field(..., min_length=1, max_length=300)
    description: str = Field(..., min_length=1)


class TicketCreateResponse(BaseModel):
    """Minimal response returned after successfully creating a ticket."""
    ticket_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TicketSummary(BaseModel):
    """
    Compact ticket representation used in the GET /api/tickets list response.
    """
    ticket_id: str
    customer_name: str
    subject: str
    status: TicketStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class TicketDetail(BaseModel):
    """
    Full ticket representation used in the GET /api/tickets/{ticket_id} response.
    Includes all fields and the list of associated notes.
    """
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    notes: list[NoteOut] = []

    model_config = {"from_attributes": True}


class TicketUpdate(BaseModel):
    """
    Schema for PUT /api/tickets/{ticket_id} request body.
    Both fields are optional so a caller can update just the status or just add a note.
    """
    status: Optional[TicketStatus] = None
    note: Optional[str] = Field(None, min_length=1, description="Optional note to append")


class TicketUpdateResponse(BaseModel):
    """Response returned after a successful ticket update."""
    success: bool = True
    updated_at: datetime

    model_config = {"from_attributes": True}
