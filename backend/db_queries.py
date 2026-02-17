"""
=============================================================================
  Week 1 — Backend Engineer
  File: db_queries.py
  Purpose: Finalized database query helpers for the Missing Person project.
=============================================================================

Provides CRUD functions used by both the frontend and the ML pipeline:
  - create_db()              → Ensures tables exist.
  - register_new_case()      → Insert a RegisteredCase.
  - new_public_case()        → Insert a PublicSubmission.
  - get_training_data()      → Fetch face-mesh data for ML training.
  - fetch_registered_cases() → List cases for the dashboard.
  - fetch_public_cases()     → List public submissions (optionally with face-mesh).
  - update_found_status()    → Mark a case as "Found" after a match.
  - get_registered_cases_count() → Dashboard metrics.
  … and more.
=============================================================================
"""

from sqlmodel import create_engine, Session, select

from data_models import RegisteredCases, PublicSubmissions


# ---------------------------------------------------------------------------
# Database engine (SQLite file in the project root)
# ---------------------------------------------------------------------------
sqlite_url = "sqlite:///sqlite_database.db"
engine = create_engine(sqlite_url, echo=False)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------
def create_db():
    """Create tables if they don't already exist."""
    try:
        RegisteredCases.__table__.create(engine)
    except Exception:
        pass  # table already exists
    try:
        PublicSubmissions.__table__.create(engine)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# INSERT helpers
# ---------------------------------------------------------------------------
def register_new_case(case_details: RegisteredCases):
    """Insert a new registered (official) missing-person case."""
    with Session(engine) as session:
        session.add(case_details)
        session.commit()


def new_public_case(public_case_details: PublicSubmissions):
    """Insert a new public sighting / submission."""
    with Session(engine) as session:
        session.add(public_case_details)
        session.commit()


# ---------------------------------------------------------------------------
# SELECT helpers — Registered Cases
# ---------------------------------------------------------------------------
def fetch_registered_cases(submitted_by: str, status: str):
    """Fetch registered cases for a given user, filtered by status string."""
    if status == "All":
        status_list = ["F", "NF"]
    elif status == "Found":
        status_list = ["F"]
    elif status == "Not Found":
        status_list = ["NF"]
    else:
        status_list = [status]

    with Session(engine) as session:
        result = session.exec(
            select(
                RegisteredCases.id,
                RegisteredCases.name,
                RegisteredCases.age,
                RegisteredCases.status,
                RegisteredCases.last_seen,
                RegisteredCases.matched_with,
            )
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status.in_(status_list))
        ).all()
        return result


def get_training_data(submitted_by: str):
    """
    Return (id, face_mesh) rows for a user's NOT-FOUND cases.
    Used by the ML pipeline to build the KNN training set.
    """
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases.id, RegisteredCases.face_mesh)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == "NF")
        ).all()
        return result


def get_registered_case_detail(case_id: str):
    """Fetch full detail of a single registered case."""
    with Session(engine) as session:
        result = session.exec(
            select(
                RegisteredCases.name,
                RegisteredCases.complainant_mobile,
                RegisteredCases.age,
                RegisteredCases.last_seen,
                RegisteredCases.birth_marks,
            ).where(RegisteredCases.id == case_id)
        ).all()
        return result


def get_registered_cases_count(submitted_by: str, status: str):
    """Return list of cases matching user + status (used for dashboard count)."""
    create_db()
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == status)
        ).all()
        return result


# ---------------------------------------------------------------------------
# SELECT helpers — Public Submissions
# ---------------------------------------------------------------------------
def fetch_public_cases(train_data: bool, status: str):
    """
    If train_data=True  → return (id, face_mesh) for ML matching.
    If train_data=False → return metadata columns for the dashboard.
    """
    if train_data:
        with Session(engine) as session:
            result = session.exec(
                select(
                    PublicSubmissions.id,
                    PublicSubmissions.face_mesh,
                ).where(PublicSubmissions.status == status)
            ).all()
            return result

    with Session(engine) as session:
        result = session.exec(
            select(
                PublicSubmissions.id,
                PublicSubmissions.status,
                PublicSubmissions.location,
                PublicSubmissions.mobile,
                PublicSubmissions.birth_marks,
                PublicSubmissions.submitted_on,
                PublicSubmissions.submitted_by,
            )
        ).all()
        return result


def get_public_case_detail(case_id: str):
    """Fetch metadata for a single public submission."""
    with Session(engine) as session:
        result = session.exec(
            select(
                PublicSubmissions.location,
                PublicSubmissions.submitted_by,
                PublicSubmissions.mobile,
                PublicSubmissions.birth_marks,
            ).where(PublicSubmissions.id == case_id)
        ).all()
        return result


def list_public_cases():
    """Return all public submissions (used in admin views)."""
    with Session(engine) as session:
        result = session.exec(select(PublicSubmissions)).all()
        return result


# ---------------------------------------------------------------------------
# UPDATE helpers
# ---------------------------------------------------------------------------
def update_found_status(register_case_id: str, public_case_id: str):
    """Mark a registered case as Found and link it to the matched public submission."""
    with Session(engine) as session:
        registered = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == str(register_case_id))
        ).one()
        registered.status = "F"
        registered.matched_with = str(public_case_id)

        public = session.exec(
            select(PublicSubmissions).where(
                PublicSubmissions.id == str(public_case_id)
            )
        ).one()
        public.status = "F"

        session.add(registered)
        session.add(public)
        session.commit()


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    create_db()
    print("✅ Database and tables ready.")
    print(f"   Registered cases (admin, NF): {len(get_registered_cases_count('admin', 'NF'))}")
    print(f"   Public submissions:           {len(list_public_cases())}")
