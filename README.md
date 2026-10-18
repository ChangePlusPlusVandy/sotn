# SOTN - Special Olympics Tennessee Intake & Routing Platform

## Project Overview
Repo for SOTN, a recruitment, intake and routing platform with:

**backend/** : FastAPI REST API (Python, PostgreSQL)  
**frontend/** : Next.js app (TypeScript, Tailwind CSS, shadcn/ui)


## Code Structure
**backend/app/core/**: App config, database session, and Clerk auth  
**backend/app/models/, schemas/, routers/**: Database tables, request/response shapes, and API endpoints (one file per entity)  
**backend/migrations/**: Alembic database migrations  
**backend/tests/**: pytest tests, run against the local database  
**frontend/src/app/**: Next.js pages, with public pages at the top level and staff pages under `admin/`  
**frontend/src/lib/api-types.ts**: TypeScript types generated from the backend API  

See `backend/README.md` for the backend layout and how to add a new entity.

## Local Setup

Follow [SETUP.md](SETUP.md) once, then use the steps below.

## Running the App

Start each layer in order, from the repo root. The backend and frontend each need their own terminal.

1. **Open Docker Desktop** and wait until it's running.
2. **Start the database**
   ```bash
   docker compose up -d
   ```
3. **Apply migrations**: only needed after pulling new files in `backend/migrations/versions/`. Safe to run anytime.
   ```bash
   cd backend
   uv run alembic upgrade head
   ```
4. **Start the backend**
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload
   ```
   Runs at `http://localhost:8000`, with interactive API docs at `http://localhost:8000/docs`.
5. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   Runs at `http://localhost:3000`. Pages that fetch data need the backend running.

## Running Tests

Tests need the database running (steps 1–3 above), but not the backend server. From `backend/`:
```bash
uv run pytest                                   # all tests
uv run pytest tests/test_inquiries.py           # one file
uv run pytest tests/test_inquiries.py::test_x   # one test
uv run pytest -k create                         # tests whose name contains "create"
```
Add `-v` to list each test as it runs. Tests roll back their changes, so your local data is untouched.

## Stopping

- **Backend and frontend:** `Ctrl+C` in their terminals.
- **Database** (from the repo root):
  ```bash
  docker compose down      # stop the database; data is kept
  docker compose down -v   # stop and delete all data (then rerun `alembic upgrade head`)
  ```
  Leaving the database running is fine. Quitting Docker Desktop or restarting your computer also stops it, so run `docker compose up -d` again next time.

## Database

**For DB Updates:** after changing a model in `backend/app/models/`
```bash
cd backend
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```
Read the generated file in `migrations/versions/` before committing it.

**View the data** (from the repo root, with the database running)
```bash
docker compose exec db psql -U sotn -d sotn
```
Inside psql: `\dt` lists tables, `\d inquiry` shows a table's columns, `SELECT * FROM inquiry;` shows its rows, and `\q` quits.

**View the data in VS Code** (with the database running)
1. Install Microsoft's [PostgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql), open the elephant icon in the sidebar, and click **Add Connection**.
2. Fill in the fields:

   | Field | Value |
   |---|---|
   | Server name | `localhost` |
   | Port | `5432` |
   | Authentication type | Password |
   | User name | `sotn` |
   | Password | `sotn` (check **Save password**) |
   | Database name | `sotn` |
   | Connection name | anything, e.g. `sotn local` |

3. Click **Connect**, then expand **sotn local → Databases → sotn → Schemas → public → Tables**.
4. Right-click a table and choose **Select Top 1000** to see its rows, or click **New Query** to run your own SQL. Ignore `alembic_version`; it only tracks which migration has run.

No tables? Run `uv run alembic upgrade head` in `backend/`.

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
