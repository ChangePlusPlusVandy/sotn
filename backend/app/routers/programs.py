import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.core.auth import get_current_staff
from app.core.db import DbSession
from app.models.inquiry import InquiryRole
from app.models.programs import Program, Region
from app.schemas.common import Page
from app.schemas.programs import (
    ProgramAdmin,
    ProgramCreate,
    ProgramPublic,
    ProgramUpdate,
)

# Public router: no authentication required
router = APIRouter(
    prefix="/programs",
    tags=["programs"],
)

# Admin router: staff authentication required
admin_router = APIRouter(
    prefix="/admin/programs",
    tags=["admin: programs"],
    dependencies=[Depends(get_current_staff)],
)


# --------------------------------------------------
# Helper: Handle database uniqueness errors
# --------------------------------------------------


def commit_program(db: DbSession):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()

        constraint = getattr(
            getattr(exc.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint == "programs_name_key":
            raise HTTPException(
                status_code=409,
                detail="Program name already exists",
            ) from exc

        raise


# --------------------------------------------------
# Public: GET /programs
# --------------------------------------------------


@router.get("", response_model=list[ProgramPublic])
def list_programs(
    db: DbSession,
    role: InquiryRole | None = None,
    region: Region | None = None,
):
    """List active programs, optionally filtered by role and region."""

    query = select(Program).where(Program.is_active.is_(True))

    if role is not None:
        query = query.where(Program.audiences.contains([role]))

    if region is not None:
        query = query.where(Program.regions.contains([region]))

    return db.scalars(query.order_by(Program.name, Program.id)).all()


# --------------------------------------------------
# Admin: GET /admin/programs
# --------------------------------------------------


@admin_router.get("", response_model=Page[ProgramAdmin])
def list_admin_programs(
    db: DbSession,
    is_active: bool | None = None,
    role: InquiryRole | None = None,
    region: Region | None = None,
    q: Annotated[
        str | None,
        Query(description="Search program name"),
    ] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    """List programs with filters and pagination."""

    query = select(Program)

    if is_active is not None:
        query = query.where(Program.is_active == is_active)

    if role is not None:
        query = query.where(Program.audiences.contains([role]))

    if region is not None:
        query = query.where(Program.regions.contains([region]))

    if q:
        query = query.where(Program.name.ilike(f"%{q}%"))

    total = db.scalar(select(func.count()).select_from(query.subquery()))

    items = db.scalars(
        query.order_by(
            Program.created_at.desc(),
            Program.id,
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return Page(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


# --------------------------------------------------
# Helper: Get program or return 404
# --------------------------------------------------


def get_program_or_404(
    db: DbSession,
    program_id: uuid.UUID,
) -> Program:
    program = db.get(Program, program_id)

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Program not found",
        )

    return program


# --------------------------------------------------
# Admin: GET /admin/programs/{program_id}
# --------------------------------------------------


@admin_router.get(
    "/{program_id}",
    response_model=ProgramAdmin,
)
def get_program(
    program: Annotated[
        Program,
        Depends(get_program_or_404),
    ],
):
    """Get one program, including internal contact details."""

    return program


# --------------------------------------------------
# Admin: POST /admin/programs
# --------------------------------------------------


@admin_router.post(
    "",
    status_code=201,
    response_model=ProgramAdmin,
)
def create_program(
    body: ProgramCreate,
    db: DbSession,
):
    """Create a program. Names must be unique."""

    existing = db.scalar(select(Program).where(Program.name == body.name))

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Program name already exists",
        )

    program = Program(**body.model_dump())

    db.add(program)
    commit_program(db)
    db.refresh(program)

    return program


# --------------------------------------------------
# Admin: PATCH /admin/programs/{program_id}
# --------------------------------------------------


@admin_router.patch(
    "/{program_id}",
    response_model=ProgramAdmin,
)
def update_program(
    body: ProgramUpdate,
    db: DbSession,
    program: Annotated[
        Program,
        Depends(get_program_or_404),
    ],
):
    """Update provided fields. Programs are deactivated, not deleted."""

    changes = body.model_dump(exclude_unset=True)

    # These database fields cannot be NULL
    required_fields = {
        "name",
        "audiences",
        "regions",
        "is_active",
    }

    for field in required_fields:
        if field in changes and changes[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )

    # Prevent renaming to another program's name
    if "name" in changes and changes["name"] != program.name:
        existing = db.scalar(select(Program).where(Program.name == changes["name"]))

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Program name already exists",
            )

    # Update only fields provided in PATCH
    for field, value in changes.items():
        setattr(program, field, value)

    commit_program(db)
    db.refresh(program)

    return program
