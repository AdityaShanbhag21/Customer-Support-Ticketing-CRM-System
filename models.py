"""
models.py
---------
Defines the SQLAlchemy ORM models (database tables) for the CRM system.

Tables:
    - Ticket : Stores all support ticket data
    - Note   : Stores notes/comments linked to a ticket (optional table)
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Ticket(Base):
    """
    Represents a customer support ticket.

    Columns:
        id             : Auto-incremented primary key (internal use)
        ticket_id      : Human-readable unique identifier (e.g., TKT-001)
        customer_name  : Full name of the customer
        customer_email : Email address of the customer
        subject        : Short title / subject of the issue
        description    : Detailed description of the issue
        status         : Current status — 'Open', 'In Progress', or 'Closed'
        created_at     : Timestamp when the ticket was created
        updated_at     : Timestamp of the last update to the ticket
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(20), unique=True, nullable=False, index=True)
    customer_name = Column(String(150), nullable=False)
    customer_email = Column(String(254), nullable=False)
    subject = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        String(20),
        nullable=False,
        default="Open"
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # One ticket can have many notes
    notes = relationship(
        "Note",
        back_populates="ticket",
        cascade="all, delete-orphan",  # deleting a ticket removes its notes
        order_by="Note.created_at"
    )

    def __repr__(self) -> str:
        return f"<Ticket id={self.ticket_id!r} status={self.status!r}>"


class Note(Base):
    """
    Represents a note or comment added to a support ticket.

    Columns:
        id         : Auto-incremented primary key
        ticket_id  : Foreign key linking to Ticket.ticket_id
        note_text  : The content of the note
        created_at : Timestamp when the note was created
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(
        String(20),
        ForeignKey("tickets.ticket_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    note_text = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Back-reference to the parent Ticket
    ticket = relationship("Ticket", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note ticket_id={self.ticket_id!r} created_at={self.created_at}>"
