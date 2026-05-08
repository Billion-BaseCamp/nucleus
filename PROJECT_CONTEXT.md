# Nucleus Project Context

This file is a quick-start context guide for engineers setting up this repository on a new device.

## What This Repository Contains

- Core SQLAlchemy models under `nucleus/models/`
- Alembic migrations under `migrations/`
- DB base/session setup in `nucleus/db/database.py`
- Python package metadata in `pyproject.toml`

The project is model-heavy. Most changes happen in model modules and migration scripts.

## First-Time Setup on a New Device

1. Clone the repo and open `nucleus/` as workspace root.
2. Create and activate a virtual environment.
3. Install dependencies (minimum for DB + migrations):
   - `pip install -e .[migrations,database]`
4. Create `.env` in project root (`nucleus/.env`) with:
   - `DATABASE_URL_SYNC=<postgres-connection-string>`
5. Verify imports:
   - `python -c "import nucleus.models; print('ok')"`
6. Verify Alembic connectivity:
   - `alembic current`

## High-Level Model Organization

- `nucleus/models/common_models/` -> shared entities (client, advisor, auth)
- `nucleus/models/advance_tax_models/` -> advance-tax domain
- `nucleus/models/itr_filling/` -> ITR filing domain
- `nucleus/models/us_tax_filing/` -> US tax filing domain
- `nucleus/models/__init__.py` -> central export/import registry used by Alembic autogenerate

## Critical Rule for Alembic Autogenerate

Alembic loads metadata from `Base.metadata`, and this project ensures model registration by importing models in `nucleus/models/__init__.py`.

If a new model class is not imported there (directly or via subpackage `__init__.py` import), autogenerate may not detect its table.

## How to Add New Models Safely (Without Disturbing Existing Models)

Follow this checklist every time:

1. **Create a new model file only in the target module**
   - Example: `nucleus/models/us_tax_filing/new_model.py`
   - Do not refactor unrelated files.

2. **Match existing ORM style in that module**
   - Use `Base` from `nucleus.db.database`
   - Use `Mapped[...]` + `mapped_column(...)`
   - Keep naming and table conventions consistent
   - Prefer string columns over enums if business logic owns enum validation

3. **Wire relationships carefully**
   - Add relationship fields only in directly related models
   - Use `back_populates` pairs
   - Keep cascade behavior aligned with sibling models

4. **Register model in subpackage exports**
   - Update module-level `__init__.py` (for example `nucleus/models/us_tax_filing/__init__.py`)
   - Add import and include class in `__all__`

5. **Register model for global metadata discovery**
   - Update `nucleus/models/__init__.py`
   - Ensure the model is imported in the appropriate block
   - Add class name in `__all__`

6. **Validate metadata registration**
   - `python -c "import nucleus.models; from nucleus.db.database import Base; print('your_table' in Base.metadata.tables)"`
   - Must print `True`

7. **Generate migration**
   - `alembic revision --autogenerate -m "add <table_name>"`
   - Inspect generated migration; verify constraints/FKs/indexes

8. **Do not change existing migration history**
   - Add new revision files only
   - Never rewrite old migrations in shared branches

## Safe Change Boundaries

- Allowed:
  - Add new model files
  - Add minimal relationship fields in directly linked models
  - Add import/export entries for registration
- Avoid unless explicitly required:
  - Renaming existing columns/tables
  - Changing existing constraints/cascades
  - Refactoring model styles across modules

## Quick Troubleshooting: "Autogenerate did not detect my table"

1. Confirm model class exists and has `__tablename__`.
2. Confirm model is imported by subpackage `__init__.py`.
3. Confirm subpackage model is imported in `nucleus/models/__init__.py`.
4. Run:
   - `python -c "import nucleus.models; from nucleus.db.database import Base; print(sorted(Base.metadata.tables.keys()))"`
5. If table missing from output, import chain is incomplete.
6. If table present but no migration diff, verify DB is on latest revision and table does not already exist.

## Useful Commands

- Format/check a model module:
  - `python -m isort nucleus/models/us_tax_filing`
  - `python -m black nucleus/models/us_tax_filing`
  - `python -m flake8 nucleus/models/us_tax_filing`
- Show current Alembic revision:
  - `alembic current`
- Create migration:
  - `alembic revision --autogenerate -m "your message"`
- Apply migration:
  - `alembic upgrade head`

## Notes for Contributors

- Keep edits small and domain-scoped.
- Preserve import order expectations where noted in file comments.
- Prioritize backward-compatible additions.
- When adding new DB structures, always verify both:
  - Python import/metadata registration
  - Alembic-generated migration correctness

