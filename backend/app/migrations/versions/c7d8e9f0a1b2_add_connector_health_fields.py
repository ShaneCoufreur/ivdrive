"""Add connector health fields (last_success_at, consecutive_failures, last_error_text)."""

from alembic import op
import sqlalchemy as sa


revision = "c7d8e9f0a1b2"
down_revision = "b7e4f1a9c2d8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE connector_sessions ADD COLUMN IF NOT EXISTS last_success_at TIMESTAMP WITH TIME ZONE")
    op.execute("ALTER TABLE connector_sessions ADD COLUMN IF NOT EXISTS consecutive_failures INTEGER NOT NULL DEFAULT 0")
    op.execute("ALTER TABLE connector_sessions ADD COLUMN IF NOT EXISTS last_error_text VARCHAR(255)")


def downgrade() -> None:
    op.drop_column("connector_sessions", "last_error_text")
    op.drop_column("connector_sessions", "consecutive_failures")
    op.drop_column("connector_sessions", "last_success_at")
