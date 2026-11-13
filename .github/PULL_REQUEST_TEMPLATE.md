## Summary

Briefly describe what this PR does.

## Changes

- Added ...
- Updated ...
- Removed ...

## Why

Explain why this change is needed.

## Testing

Describe how you tested the changes.

**Backend** (`cd backend`)

- [ ] Ran `uv run ruff check .`
- [ ] Ran `uv run ruff format --check .`
- [ ] Ran `uv run pytest`

**Frontend** (`cd frontend`)

- [ ] Ran `npm run lint`
- [ ] Ran `npm run typecheck`
- [ ] Ran `npm run build` (not in CI, but catches prerender errors)

- [ ] Tested manually

Additional testing notes:

## Screenshots

Include screenshots if this PR changes the UI.

If there are no UI changes, write:

N/A

## Database Changes

- [ ] No database changes
- [ ] Adds a new Alembic migration
- [ ] Migration `down_revision` points at the current head on `main` (CI fails on multiple heads)

If applicable, describe the migration:

## API Changes

- [ ] No API changes
- [ ] Changed backend request/response shapes and regenerated frontend types with `npm run api:types`

## Environment Variables

- [ ] No new environment variables
- [ ] New variables added to `backend/.env.example`
- [ ] New variables added to `frontend/.env.example`

List any new variables:

## Related Issue / Task

Closes #

or

Related to:

## Notes for Reviewer

Anything the reviewer should pay particular attention to.

## Checklist

- [ ] My branch is up to date with `main`
- [ ] I did not commit secrets or `.env` files
- [ ] I kept the PR focused on one task
- [ ] I updated Pydantic schemas (`app/schemas`) and frontend types where needed
