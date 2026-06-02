from unittest.mock import MagicMock

from app.services.tracing.trace_logger import AgentTraceLogger


def test_trace_logger_records_success() -> None:
    db = MagicMock()
    user = MagicMock()
    user.id = "user_123"

    logger = AgentTraceLogger(db=db, user=user, query="test query")

    with logger as active_logger:
        trace = active_logger.mark_success(
            response="test response",
            prompt_tokens=10,
            completion_tokens=5,
        )

    assert trace.status == "success"
    assert trace.response == "test response"
    assert trace.prompt_tokens == 10
    assert trace.completion_tokens == 5
    assert trace.latency_ms is not None
    db.add.assert_called()
    db.commit.assert_called()
