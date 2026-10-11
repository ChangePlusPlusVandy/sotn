from pydantic import BaseModel


class Page[T](BaseModel):
    """Response shape for every paginated list endpoint."""

    items: list[T]
    total: int
    page: int
    page_size: int
