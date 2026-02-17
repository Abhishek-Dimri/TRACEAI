"""
=============================================================================
  Week 1 — Backend Engineer
  File: migrations.py
  Purpose: Database migration / table-creation helper.
=============================================================================

Run this script once to ensure the SQLite database and all tables exist.
It is safe to run multiple times (CREATE IF NOT EXISTS semantics).

Usage:
    python migrations.py
=============================================================================
"""

from sqlmodel import create_engine, SQLModel
from data_models import RegisteredCases, PublicSubmissions   # noqa: F401


DB_URL = "sqlite:///sqlite_database.db"


def run_migrations():
    """Create all tables defined in data_models.py."""
    engine = create_engine(DB_URL, echo=True)
    SQLModel.metadata.create_all(engine)
    print("\n✅ Migration complete — all tables are up to date.")


if __name__ == "__main__":
    run_migrations()
