"""
=============================================================================
  Week 1 — Backend Engineer
  File: seed_data.py
  Purpose: Insert sample / placeholder data so other team members can
           test their code without needing real images.
=============================================================================

Generates dummy face-mesh vectors (random floats) and inserts a handful of
RegisteredCases and PublicSubmissions rows.

Usage:
    python seed_data.py
=============================================================================
"""

import json
import random
from uuid import uuid4
from datetime import datetime

from sqlmodel import create_engine, Session, SQLModel
from data_models import RegisteredCases, PublicSubmissions


DB_URL = "sqlite:///sqlite_database.db"
engine = create_engine(DB_URL)

# Number of landmarks MediaPipe returns (468 landmarks × 3 coords = 1404 floats)
NUM_FEATURES = 1404


def random_face_mesh() -> str:
    """Return a JSON string of 1404 random floats simulating face-mesh output."""
    return json.dumps([round(random.uniform(0, 1), 6) for _ in range(NUM_FEATURES)])


def seed():
    """Insert sample rows into both tables."""
    SQLModel.metadata.create_all(engine)

    registered_samples = [
        RegisteredCases(
            id=str(uuid4()),
            submitted_by="Gagandeep Singh",
            name="Ravi Kumar",
            father_name="Suresh Kumar",
            age="12",
            address="Sector 62, Noida",
            last_seen="Near City Mall, 2026-01-15",
            birth_marks="Small scar on left cheek",
            adhaar_card="123456789012",
            complainant_name="Suresh Kumar",
            complainant_mobile="9876543210",
            face_mesh=random_face_mesh(),
            submitted_on=datetime(2026, 1, 15, 10, 30),
            status="NF",
            matched_with=None,
        ),
        RegisteredCases(
            id=str(uuid4()),
            submitted_by="Gagandeep Singh",
            name="Priya Sharma",
            father_name="Ramesh Sharma",
            age="8",
            address="Lajpat Nagar, Delhi",
            last_seen="Central Park, 2026-01-20",
            birth_marks="Mole on right hand",
            adhaar_card="987654321098",
            complainant_name="Ramesh Sharma",
            complainant_mobile="9123456780",
            face_mesh=random_face_mesh(),
            submitted_on=datetime(2026, 1, 20, 14, 0),
            status="NF",
            matched_with=None,
        ),
        RegisteredCases(
            id=str(uuid4()),
            submitted_by="Gagandeep Singh",
            name="Amit Verma",
            father_name="Dinesh Verma",
            age="15",
            address="MG Road, Bangalore",
            last_seen="Bus Stand, 2026-02-01",
            birth_marks="None",
            adhaar_card="111222333444",
            complainant_name="Dinesh Verma",
            complainant_mobile="9988776655",
            face_mesh=random_face_mesh(),
            submitted_on=datetime(2026, 2, 1, 9, 0),
            status="NF",
            matched_with=None,
        ),
    ]

    public_samples = [
        PublicSubmissions(
            id=str(uuid4()),
            submitted_by="Anonymous Citizen",
            face_mesh=random_face_mesh(),
            location="Railway Station, Noida",
            mobile="9000000001",
            email="citizen1@example.com",
            birth_marks="Scar on cheek",
            status="NF",
            submitted_on=datetime(2026, 2, 5, 16, 45),
        ),
        PublicSubmissions(
            id=str(uuid4()),
            submitted_by="NGO Volunteer",
            face_mesh=random_face_mesh(),
            location="Shelter Home, Delhi",
            mobile="9000000002",
            email="volunteer@ngo.org",
            birth_marks="Mole on hand",
            status="NF",
            submitted_on=datetime(2026, 2, 6, 11, 30),
        ),
    ]

    with Session(engine) as session:
        for case in registered_samples:
            session.add(case)
        for sub in public_samples:
            session.add(sub)
        session.commit()

    print(f"✅ Seeded {len(registered_samples)} registered cases.")
    print(f"✅ Seeded {len(public_samples)} public submissions.")


if __name__ == "__main__":
    seed()
