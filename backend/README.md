# Week 1 — Backend & Data Engineer

## Objective
Finalize the database schema, set up migration scripts, create the `resources/` layout,
and insert sample placeholder data so the ML and Frontend teams can begin development
independently.

## Files Delivered
| File              | Purpose                                                    |
|-------------------|------------------------------------------------------------|
| `data_models.py`  | SQLModel table definitions (`RegisteredCases`, `PublicSubmissions`) with full field documentation. |
| `db_queries.py`   | All CRUD query helpers consumed by the app and ML pipeline.|
| `migrations.py`   | One-command script to create / update tables in SQLite.    |
| `seed_data.py`    | Inserts 3 registered cases + 2 public submissions with dummy face-mesh vectors. |

## How to Run
```bash
cd college_project/backend_engineer
python migrations.py      # Create tables
python seed_data.py        # Populate sample data
python db_queries.py       # Quick self-test
```

## Key Decisions
- **SQLite** chosen for portability (single file `sqlite_database.db`).
- **face_mesh** stored as a JSON string of 1404 floats (468 landmarks × 3 coordinates).
- UUIDs generated as plain strings for SQLite compatibility.

## Next Week Preview
- Prototype CCTV ingestion script (`scripts/ingest_cctv.py`).
