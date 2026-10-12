# SOTN - Special Olympics Tennessee Intake & Routing Platform

## Project Overview
Repo for SOTN, a recruitment, intake and routing platform with:

**backend/** : FastAPI REST API (Python, PostgreSQL)
**frontend/** : Next.js app (TypeScript, Tailwind CSS, shadcn/ui)

Product context and requirements live in **docs/**, starting with `docs/working-prd.md`.

## Code Structure
**backend/app/core/**: App config, database session, and Clerk auth
**backend/app/models/, schemas/, routers/**: Database tables, request/response shapes, and API endpoints (one file per entity)
**backend/migrations/**: Alembic database migrations
**backend/tests/**: pytest tests, run against the local database
**frontend/src/app/**: Next.js pages, with public pages at the top level and staff pages under `admin/`
**frontend/src/lib/api-types.ts**: TypeScript types generated from the backend API

See `backend/README.md` for the backend layout and how to add a new entity.

## Local Setup

Requires [Docker Desktop](https://docs.docker.com/desktop), [uv](https://docs.astral.sh/uv/getting-started/installation/), and Node 22+.

### Install dependencies
```bash
cd backend
uv sync
cd ../frontend
npm install
```

### Start backend
Set up the database first (see below).
```bash
cd backend
uv run uvicorn app.main:app --reload
```
Runs at `http://localhost:8000`, with interactive API docs at `http://localhost:8000/docs`.

### Start frontend
```bash
cd frontend
npm run dev
```
Runs at `http://localhost:3000`.

## PostgreSQL Database Setup

- **Docker Desktop** must be installed and running
  - Required for the local PostgreSQL database

1. **Start and stop local PostgreSQL** (from the repo root)
   ```bash
   docker compose up -d
   docker compose down
   ```
   This creates a local database at `postgresql://sotn:sotn@localhost:5432/sotn`

2. **Configure Environment Variables**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   ```
   - `backend/.env`: `DATABASE_URL` is already set for the local database. Set `CLERK_ISSUER` to the Clerk app's Frontend API URL (Clerk dashboard > API keys).
   - `frontend/.env.local`: add the Clerk publishable and secret keys. The app won't load without them. Use the team's Clerk app, or run `npx clerk@latest init` for temporary dev keys.

3. **Create the tables**
   ```bash
   cd backend
   uv run alembic upgrade head
   ```

   **For DB Updates:** after changing a model in `backend/app/models/`
   ```bash
   cd backend
   uv run alembic revision --autogenerate -m "describe the change"
   uv run alembic upgrade head
   ```
   Read the generated file in `migrations/versions/` before committing it.

## Notes

Backend uses FastAPI, SQLAlchemy, Alembic, PostgreSQL, and Clerk auth. Frontend uses Next.js, Clerk, Tailwind, and shadcn/ui. Staff sign in with Clerk; public visitors never need an account. Any signed-in Clerk user counts as staff for now, so keep Clerk sign-ups set to invitation only.

Before each push, run these for code consistency for all devs. CI runs the same checks on every pull request.
```bash
cd backend
uv run ruff format .
uv run ruff check .
uv run pytest

cd ../frontend
npm run lint
npm run typecheck
```
After changing backend endpoints, run `npm run api:types` in `frontend/` (with the backend running) to update the generated types.

**Documentation Links For Reference:**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [uv Docs](https://docs.astral.sh/uv/)
- [Next.js Docs](https://nextjs.org/docs)
- [Clerk Auth Docs](https://clerk.com/docs)
- [shadcn/ui Docs](https://ui.shadcn.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Docker Desktop Docs](https://docs.docker.com/desktop/)

test
