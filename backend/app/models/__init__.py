# Import every model here so Alembic autogenerate can see its table.
from app.models.inquiry import Inquiry  # noqa: F401
from app.models.inquiry_activity import InquiryActivity as InquiryActivity
from app.models.inquiry_note import InquiryNote  # noqa: F401
from app.models.programs import Program  # noqa: F401
from app.models.resource import Resource  # noqa: F401
