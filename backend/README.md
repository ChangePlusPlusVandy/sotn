# Backend

Setup is in the [root README](../README.md). This file covers how the code is laid out and how to add to it.

## Layout

```
app/
  main.py          App setup: CORS, routers, /health
  core/            Infrastructure shared by every feature
    config.py      Settings, read from .env
    db.py          Engine and the DbSession dependency
    auth.py        get_current_staff / CurrentStaff: verifies the Clerk session token
  models/          SQLAlchemy tables, one file per entity
    base.py        Base class and str_enum() for enum columns
    __init__.py    Imports every model so Alembic can see it
  schemas/         Pydantic request and response shapes; common.py has Page[T]
  routers/         Routes, one file per entity (the route function is the controller)
migrations/        Alembic; versions/ is generated from app/models/
tests/             pytest; each test runs in a rolled-back transaction on empty tables
```

**Reference implementation:** inquiries. Copy its patterns:
- `app/models/inquiry.py`
- `app/schemas/inquiry.py`
- `app/routers/inquiries.py`
- `tests/test_inquiries.py`

## Adding an entity

1. **Model:** add `app/models/<entity>.py` and import it in `app/models/__init__.py`. Without that import, Alembic won't see the table.
2. **Migration:** run `uv run alembic revision --autogenerate -m "create <entity>"`. Read the generated file before committing; autogenerate misses some changes, such as column renames. Then run `uv run alembic upgrade head`.
3. **Schemas:** add `app/schemas/<entity>.py` with separate classes for each shape: `Create` (request), `Read` (response, `from_attributes=True`) and `Update` (all fields optional).
4. **Routes:** add `app/routers/<entity>.py` and include its router in `app/main.py`.
5. **Tests:** add `tests/test_<entity>.py`. Cover the success path, validation errors (422), not found (404) and unauthenticated access (401).
6. **Frontend types:** with the backend running, run `npm run api:types` in `frontend/`.

## Conventions

- **Public vs. staff routes:** staff routes live on a router with `prefix="/admin/..."` and `dependencies=[Depends(get_current_staff)]`, so every route on it requires sign-in. Add `staff_id: CurrentStaff` to a route only when you need the user ID. Public responses must not echo back personal data; see `InquiryConfirmation`.
- **Naming:** a submitted record is an **inquiry** in code, the database and the API (`Inquiry`, `InquiryRead`, `/admin/inquiries`). "Intake" refers only to the public form and user-facing copy.
- **Enums:** `StrEnum` classes with lowercase values, stored through `str_enum()` so the database holds the same values as the API.
- **Partial updates:** `body.model_dump(exclude_unset=True)` changes only the fields the client sent.
- **Lists:** return `Page[ReadSchema]`, and paginate with `page` and `page_size` query params.
- **No hard deletes for people or inquiries:** the PRD requires a documented privacy workflow instead.
- **Tests:** use `client` for public requests and `staff_client` to act as a signed-in staff member. They require `alembic upgrade head` to have run against the database in `DATABASE_URL`.
- **Migrations:** when two PRs both add migrations, the second to merge must rebase and set its `down_revision` to the other's revision. CI fails if there's more than one head.
