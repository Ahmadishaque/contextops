from time import perf_counter
from typing import Self

from sqlalchemy.orm import Session

from app.db import base as _db_base  # noqa: F401
from app.db.models.trace import Trace
from app.db.models.user import User


class AgentTraceLogger:
    def __init__(self, db: Session, user: User, query: str) -> None:
        self.db = db
        self.user = user
        self.query = query
        self.start_time = perf_counter()
        self.trace: Trace | None = None

    def __enter__(self) -> Self:
        self.trace = Trace(
            user_id=self.user.id,
            query=self.query,
            status="running",
        )
        self.db.add(self.trace)
        self.db.flush()
        return self

    def mark_success(
        self,
        response: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
    ) -> Trace:
        if self.trace is None:
            raise RuntimeError("Trace logger was not started")

        self.trace.response = response
        self.trace.status = "success"
        self.trace.latency_ms = self._elapsed_ms()
        self.trace.prompt_tokens = prompt_tokens
        self.trace.completion_tokens = completion_tokens

        self.db.add(self.trace)
        self.db.commit()
        self.db.refresh(self.trace)

        return self.trace

    def mark_failure(self, error_message: str) -> Trace:
        if self.trace is None:
            raise RuntimeError("Trace logger was not started")

        self.trace.response = error_message
        self.trace.status = "failure"
        self.trace.latency_ms = self._elapsed_ms()

        self.db.add(self.trace)
        self.db.commit()
        self.db.refresh(self.trace)

        return self.trace

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_value is not None and self.trace is not None:
            self.mark_failure(str(exc_value))

        return False

    def _elapsed_ms(self) -> float:
        return round((perf_counter() - self.start_time) * 1000, 2)
