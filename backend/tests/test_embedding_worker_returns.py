"""Regression tests for backend/app/services/embedding_worker.py — process_one return shape.

Background
----------
PR #167 (fix/embedding-producer-guard) updated process_one()'s signature to
return `(success, permanent_failure, message)` — a 3-tuple — so that callers
can detect permanent failures (no source data, unknown content_type) and
delete the queue row immediately instead of incrementing attempts.

The signature + docstring + 3 of 5 return paths were updated correctly, but
**two return paths kept returning 2-tuples**:

    return True, "ok"                            # success branch
    return False, f"store error: {e!r}"          # exception branch in process_one

In production this crashed every worker tick with
    ValueError: not enough values to unpack (expected 3, got 2)
at `process_pending_batch`, leaving 1309 queue rows pending and 455 failed.

These tests pin the 3-tuple contract for every code path in process_one.

Run:
    cd backend && pytest tests/test_embedding_worker_returns.py -v
"""

import asyncio
import sys
import types
from types import SimpleNamespace

import pytest

from app.services import embedding_worker


class _FakeSession:
    """Minimal stub — only the await .execute(...) calls hit this."""

    async def execute(self, *_args, **_kwargs):
        return SimpleNamespace(fetchone=lambda: None)

    async def commit(self):
        return None


def _install_fake_ai_embeddings(monkeypatch, generate_behavior):
    """Replace `app.services.ai_embeddings.generate_embedding` in sys.modules.

    Direct monkeypatch.setattr on the dotted path triggers pytest's lazy
    import and fails because httpx isn't installed in the test env. Patching
    sys.modules is the clean fix.
    """
    async def fake_generate_embedding(_chunk):
        return generate_behavior(_chunk)

    fake_mod = types.ModuleType("app.services.ai_embeddings")
    fake_mod.generate_embedding = fake_generate_embedding
    monkeypatch.setitem(sys.modules, "app.services.ai_embeddings", fake_mod)


async def _builder_returning(builder_returns):
    if isinstance(builder_returns, BaseException):
        raise builder_returns
    return builder_returns


@pytest.mark.parametrize(
    "branch, content_type, builder_returns, generate_behavior, expected",
    [
        # success path — builder returns chunk+meta, embedding returns (vec, model)
        (
            "success",
            "vehicle_summary",
            ("chunk text", {"k": "v"}),
            lambda _c: ([0.0] * 768, "model-x"),
            (True, False, "ok"),
        ),
        # store-error path — generate_embedding raises
        (
            "store_error",
            "vehicle_summary",
            ("chunk text", {"k": "v"}),
            lambda _c: (_ for _ in ()).throw(RuntimeError("simulated provider failure")),
            (False, False, "store error: RuntimeError('simulated provider failure')"),
        ),
        # unknown content_type — short-circuit before builder is called
        (
            "unknown_content_type",
            "definitely_not_registered",
            None,
            lambda _c: None,
            (False, True, "unknown content_type=definitely_not_registered"),
        ),
        # builder raises an exception
        (
            "builder_error",
            "vehicle_summary",
            RuntimeError("builder boom"),
            lambda _c: None,
            (False, False, "builder error: RuntimeError('builder boom')"),
        ),
        # builder returns falsy → no source data, permanent
        (
            "no_source_data",
            "vehicle_summary",
            None,
            lambda _c: None,
            (False, True, "no source data for vehicle_summary/veh:veh-1"),
        ),
    ],
)
def test_process_one_returns_3_tuple_for_every_branch(
    monkeypatch, branch, content_type, builder_returns, generate_behavior, expected
):
    """Every code path in process_one must return a 3-tuple (success, permanent, msg).

    This is the regression test for the v1.1.2.1 / v1.1.2.2 worker crash:
    two of five return paths were returning 2-tuples and crashing every tick.
    """
    async def fake_builder(_session, _vid):
        return await _builder_returning(builder_returns)

    fake_registry = {"vehicle_summary": ("summary", fake_builder)}
    monkeypatch.setattr(embedding_worker, "CONTENT_TYPES", fake_registry)
    _install_fake_ai_embeddings(monkeypatch, generate_behavior)
    monkeypatch.setattr(embedding_worker, "text_to_embedding", lambda _c: [0.0] * 768)
    monkeypatch.setattr(embedding_worker, "EMBEDDING_PROVIDER", "test")

    content_id = "veh:veh-1" if branch != "unknown_content_type" else "x:1"

    result = asyncio.run(
        embedding_worker.process_one(
            session=_FakeSession(),
            queue_id="00000000-0000-0000-0000-000000000001",
            user_id="00000000-0000-0000-0000-000000000002",
            vehicle_id="00000000-0000-0000-0000-000000000003",
            content_type=content_type,
            content_id=content_id,
            priority=0,
        )
    )

    # Shape contract: must be a 3-tuple of (bool, bool, str)
    assert isinstance(result, tuple), f"branch={branch}: result is not a tuple"
    assert len(result) == 3, f"branch={branch}: expected 3-tuple, got {len(result)}-tuple"
    success, permanent, msg = result
    assert isinstance(success, bool), f"branch={branch}: success is not bool"
    assert isinstance(permanent, bool), f"branch={branch}: permanent is not bool"
    assert isinstance(msg, str), f"branch={branch}: msg is not str"
    assert (success, permanent, msg) == expected, (
        f"branch={branch}: returned {result!r}, expected {expected!r}"
    )