# Import every model here so Alembic autogenerate can see its table.
from app.models.inquiry import Inquiry  # noqa: F401
from app.models.inquiry_activity import InquiryActivity as InquiryActivity
