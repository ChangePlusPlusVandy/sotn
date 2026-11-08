"""add inquiry region

Revision ID: a1b2c3d4e5f6
Revises: f570598a117d
Create Date: 2026-11-08 01:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f570598a117d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "inquiries",
        sa.Column(
            "region",
            sa.Enum(
                "east",
                "middle",
                "west",
                name="region",
                native_enum=False,
                length=32,
            ),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("inquiries", "region")
