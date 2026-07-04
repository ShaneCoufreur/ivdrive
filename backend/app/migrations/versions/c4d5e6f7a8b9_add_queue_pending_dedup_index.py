"""add unique partial index on ai_embeddings_queue (content_type, content_id) WHERE status = 'pending'

Revision ID: c4d5e6f7a8b9
Revises: b1c2d3e4f5g6
Create Date: 2026-07-04 17:08:00.000000

Background
----------
The collector's enqueue path calls ``queue_content()`` in
``app/services/ai_embeddings.py``, which executes::

    INSERT INTO ai_embeddings_queue (...)
    VALUES (...)
    ON CONFLICT DO NOTHING

There is no UNIQUE or PRIMARY KEY constraint on
``(ai_embeddings_queue.content_type, ai_embeddings_queue.content_id)``,
so Postgres has nothing for ``ON CONFLICT`` to match against. **Every
collector poll cycle inserts new pending rows for already-pending items**
and the queue grows unboundedly while the worker drains at a steady
batch_size/tick.

In production this manifested as 1462 pending rows for only ~70 unique
``(content_type, content_id)`` pairs (a ~21× duplication factor).
Captured 2026-07-04 ~14:00 UTC:

  - enqueue rate: ~21 rows/min (poll every 5 min × 14 vehicles × 7 types)
  - drain rate:   ~10 rows/min (batch_size=50, tick every 5 min)
  - net growth:   +11 rows/min until the queue floods

This migration adds a partial unique index that scopes ``ON CONFLICT``
to the right slice — only rows currently in ``pending`` state matter
for the collector dedup. Completed/failed rows are kept out of the
unique constraint so the historical log isn't constrained.

Why partial: a non-partial unique index on ``(content_type, content_id)``
would FORCE the schema to keep only one row per pair across all states,
which would break the historical audit trail of past failed/completed
work. We only need to collapse the *currently-pending* duplicates, so
``WHERE status = 'pending'`` is the right granularity.

Why ``CREATE INDEX`` (not ``CONCURRENTLY``): ``ai_embeddings_queue`` is
small (couple thousand rows), the index builds in <100ms with a Share
lock. The complexity of a CONCURRENTLY migration isn't worth it here.

Production deployment note
-------------------------
The v1.1.2.4 deploy does **not** run ``alembic upgrade head``. The
production schema is already in sync because the same
``CREATE UNIQUE INDEX`` was applied directly via psql on
2026-07-04 ~14:08 UTC, before this PR landed. The migration file is
kept in the repo so dev / fresh-install environments get the index
via normal alembic flow; production ops skip it.

The migration uses ``IF NOT EXISTS`` so it is safe to re-run if the
index already exists on the target DB.

After this migration::

    INSERT ... ON CONFLICT (content_type, content_id)
        WHERE status = 'pending' DO NOTHING
    -- now matches the new unique index and silently collapses
    -- duplicate pending rows.
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c4d5e6f7a8b9"
# Chain off the v1.1.2.2 merge head which is the production
# alembic_version at the time of writing. Multiple other heads exist
# on main but they represent pending migrations not yet applied to
# production (independent of this change). New migrations that need
# to chain through them should add their own merge head first.
down_revision: Union[str, None] = "b1c2d3e4f5g6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the partial unique index that makes ``queue_content``'s
    ``ON CONFLICT`` clause actually dedup duplicate pending rows.

    Steps:
      1. Deduplicate existing pending rows so the partial unique
         index can be created without violating the constraint.
         Keeps the OLDEST row per (content_type, content_id) pair.
      2. Create the partial unique index (``IF NOT EXISTS`` makes
         this safe to re-run on a DB that already has the index).
    """
    # Step 1: dedup existing pending rows (keep oldest per pair).
    # Required because CREATE UNIQUE INDEX fails if pre-existing
    # rows already violate the constraint. In production this was
    # already done manually before this migration landed; on dev /
    # staging / fresh-install the migration is self-sufficient.
    op.execute(
        """
        DELETE FROM ai_embeddings_queue a
        WHERE a.status = 'pending'
          AND EXISTS (
              SELECT 1 FROM ai_embeddings_queue b
              WHERE b.status = 'pending'
                AND b.content_type = a.content_type
                AND b.content_id = a.content_id
                AND b.created_at < a.created_at
          )
        """
    )

    # Step 2: create the partial unique index.
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_queue_pending_dedup
            ON ai_embeddings_queue (content_type, content_id)
            WHERE status = 'pending'
        """
    )


def downgrade() -> None:
    """Drop the partial unique index. Queue goes back to allowing
    duplicate pending rows — collector dedup behaviour reverts to
    re-enqueueing every poll cycle (pre-fix state).
    """
    op.execute("DROP INDEX IF EXISTS idx_queue_pending_dedup")