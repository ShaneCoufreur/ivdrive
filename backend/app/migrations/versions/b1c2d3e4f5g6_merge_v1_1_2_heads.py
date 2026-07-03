"""merge v1.1.2 alembic heads.

Production was blocked on `alembic upgrade head` with:

    Multiple head revisions are present for given argument 'head'

Two heads existed after merging release/v1.1.2 -> main:
  - c7d8e9f0a1b2 (v1.1.1 connector health fields — already in prod)
  - a1b2c3d4e5g7 (v1.1.2 battery SoH ops model — needs to apply)

Both chains share a common ancestor at b2c3d4e5f6a8 but were never
re-unified by a merge migration in v1.1.2.

This is a pure merge: no schema changes, alembic just records that
both lineages are now unified.

Revision ID: b1c2d3e4f5g6
Revises: c7d8e9f0a1b2, a1b2c3d4e5g7
Create Date: 2026-07-03 17:40:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1c2d3e4f5g6"
down_revision: Union[str, tuple, None] = ("c7d8e9f0a1b2", "a1b2c3d4e5g7")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Pure merge — no schema changes.
    pass


def downgrade() -> None:
    # Pure merge — no schema changes.
    pass