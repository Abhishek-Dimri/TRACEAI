"""
=============================================================================
  Week 1 — Backend Engineer
  File: data_models.py
  Purpose: Finalized database schema for the Missing Person project.
=============================================================================

This file defines the two core tables used across the application:

  1. RegisteredCases  — Cases filed by authorized users (police / admin).
  2. PublicSubmissions — Sightings / photos submitted by the general public.

Both tables store face-mesh landmarks as a JSON string so the ML pipeline
can consume them directly without touching raw image files.
=============================================================================
"""

from uuid import uuid4
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------------------
# Table 1 — Registered (official) missing-person cases
# ---------------------------------------------------------------------------
class RegisteredCases(SQLModel, table=True):
    """An official missing-person case registered by an authorized user."""

    __table_args__ = {"extend_existing": True}

    # Primary key — UUID string
    id: str = Field(
        primary_key=True,
        default_factory=lambda: str(uuid4()),
        nullable=False,
        description="Unique case identifier (UUID).",
    )

    # Who submitted this case (username from login_config.yml)
    submitted_by: str = Field(
        max_length=64, nullable=False, description="Username of the submitter."
    )

    # Missing person details
    name: str = Field(max_length=128, nullable=False, description="Full name.")
    father_name: Optional[str] = Field(
        default=None, max_length=128, description="Father's name."
    )
    age: Optional[str] = Field(default=None, max_length=8, description="Age.")
    address: str = Field(default="", max_length=512, description="Last known address.")
    last_seen: str = Field(
        default="", max_length=64, description="Last seen location / date."
    )
    birth_marks: str = Field(
        default="", max_length=512, description="Identifying marks."
    )
    adhaar_card: str = Field(default="", max_length=12, description="Aadhaar number.")

    # Complainant details
    complainant_name: str = Field(
        default="", max_length=128, description="Complainant's name."
    )
    complainant_mobile: Optional[str] = Field(
        default=None, max_length=10, description="Complainant's phone."
    )

    # Face-mesh vector stored as JSON string  (1404 floats for 468 landmarks × 3)
    face_mesh: str = Field(
        nullable=False, description="JSON-encoded face-mesh landmark vector."
    )

    # Metadata
    submitted_on: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of submission."
    )
    status: str = Field(
        max_length=16,
        nullable=False,
        description="Case status: 'NF' (Not Found) or 'F' (Found).",
    )
    matched_with: Optional[str] = Field(
        default=None,
        description="UUID of the matched PublicSubmission (if found).",
    )


# ---------------------------------------------------------------------------
# Table 2 — Public sightings / submissions
# ---------------------------------------------------------------------------
class PublicSubmissions(SQLModel, table=True):
    """A sighting or photo submitted by a member of the public."""

    __table_args__ = {"extend_existing": True}

    id: str = Field(
        primary_key=True,
        default_factory=lambda: str(uuid4()),
        nullable=False,
        description="Unique submission identifier (UUID).",
    )

    submitted_by: Optional[str] = Field(
        default=None, max_length=128, description="Name of submitter."
    )

    # Face-mesh vector stored as JSON string
    face_mesh: str = Field(
        nullable=False, description="JSON-encoded face-mesh landmark vector."
    )

    location: Optional[str] = Field(
        default=None, max_length=128, description="Where the person was seen."
    )
    mobile: str = Field(
        default="", max_length=10, description="Contact phone number."
    )
    email: Optional[str] = Field(
        default=None, max_length=64, description="Contact email."
    )
    birth_marks: Optional[str] = Field(
        default=None, max_length=512, description="Identifying marks noticed."
    )
    status: str = Field(
        max_length=16,
        nullable=False,
        description="Status: 'NF' (Not Found) or 'F' (Found / matched).",
    )

    submitted_on: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of submission."
    )


# ---------------------------------------------------------------------------
# Quick self-test: create tables in an in-memory SQLite DB
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from sqlmodel import create_engine

    engine = create_engine("sqlite:///test_schema.db", echo=True)
    SQLModel.metadata.create_all(engine)
    print("\n✅ Schema created successfully in test_schema.db")
