import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, or_, select

from app.core.auth import get_current_staff
from app.core.db import DbSession
from app.models.inquiry import InquiryRole
from app.models.resource import Resource, ResourceKind
from app.schemas.common import Page
from app.schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate

# Public routes: only published resources are ever visible here.
router = APIRouter(prefix="/resources", tags=["resources"])

# Staff routes: the router-level dependency rejects unauthenticated requests on every route.
admin_router = APIRouter(
    prefix="/admin/resources",
    tags=["admin: resources"],
    dependencies=[Depends(get_current_staff)],
)


def paginate(db: DbSession, query, page: int, page_size: int) -> Page[ResourceRead]:
    # Count all matching rows before pagination, so the client knows how many pages exist.
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        query.order_by(Resource.created_at.desc(), Resource.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)


@router.get("", response_model=Page[ResourceRead])
def list_published_resources(
    db: DbSession,
    role: Annotated[
        InquiryRole | None, Query(description="Only resources for this role")
    ] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    """List published resources for the public results page, optionally for one role."""

    query = select(Resource).where(Resource.is_published.is_(True))
    if role:
        query = query.where(Resource.audiences.contains([role]))
    return paginate(db, query, page, page_size)


@admin_router.get("", response_model=Page[ResourceRead])
def list_resources(
    db: DbSession,
    kind: ResourceKind | None = None,
    is_published: bool | None = None,
    q: Annotated[str | None, Query(description="Search title or description")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    """List all resources, published or not, newest first, with optional filters and search."""

    query = select(Resource)
    if kind:
        query = query.where(Resource.kind == kind)
    if is_published is not None:
        query = query.where(Resource.is_published.is_(is_published))
    if q:
        query = query.where(
            or_(
                Resource.title.ilike(f"%{q}%"),
                Resource.description.ilike(f"%{q}%"),
            )
        )
    return paginate(db, query, page, page_size)


# helper for the routes that act on one resource
def get_resource_or_404(db: DbSession, resource_id: uuid.UUID) -> Resource:
    resource = db.get(Resource, resource_id)
    if resource is None:
        raise HTTPException(404, "Resource not found")
    return resource


@admin_router.post("", status_code=201, response_model=ResourceRead)
def create_resource(body: ResourceCreate, db: DbSession):
    """Create a resource. New resources are unpublished unless is_published is sent."""

    resource = Resource(**body.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)  # reload server-set values (created_at, updated_at)
    return resource


@admin_router.get("/{resource_id}", response_model=ResourceRead)
def get_resource(resource: Annotated[Resource, Depends(get_resource_or_404)]):
    """Get one resource."""

    return resource


@admin_router.patch("/{resource_id}", response_model=ResourceRead)
def update_resource(
    body: ResourceUpdate,
    db: DbSession,
    resource: Annotated[Resource, Depends(get_resource_or_404)],
):
    """Update only the fields sent in the body."""

    # exclude_unset: only fields the client sent, so omitted fields stay unchanged.
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return resource


@admin_router.delete("/{resource_id}", status_code=204)
def delete_resource(
    db: DbSession,
    resource: Annotated[Resource, Depends(get_resource_or_404)],
):
    """Permanently delete a resource. Resources hold no personal data, so this is a hard delete."""

    db.delete(resource)
    db.commit()
    return Response(status_code=204)
