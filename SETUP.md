# First-Time Setup

Do these steps once, when you first clone the repo. To run the app day to day, see the [README](README.md).

Requires [Docker Desktop](https://docs.docker.com/desktop), [uv](https://docs.astral.sh/uv/getting-started/installation/), and Node 22+.

1. **Install dependencies**
   ```bash
   cd backend
   uv sync
   cd ../frontend
   npm install
   ```

2. **Configure environment variables** (from the repo root)
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   ```
   - `backend/.env`: `DATABASE_URL` is already set for the local database. Set `CLERK_ISSUER` to the Clerk app's Frontend API URL (Clerk dashboard > API keys).
   - `frontend/.env.local`: add the Clerk publishable and secret keys. The app won't load without them. Use the team's Clerk app, or run `npx clerk@latest init` for temporary dev keys.

3. **Start the database** (Docker Desktop must be running; from the repo root)
   ```bash
   docker compose up -d
   ```
   This creates a local PostgreSQL database at `postgresql://sotn:sotn@localhost:5432/sotn`.

4. **Create the tables**
   ```bash
   cd backend
   uv run alembic upgrade head
   ```

Setup is done. Continue with [Running the app](README.md#running-the-app) in the README.
