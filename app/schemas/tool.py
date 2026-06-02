from typing import Any

from pydantic import BaseModel, Field


class ToolMetadata(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any]


class ToolRunRequest(BaseModel):
    tool_name: str = Field(..., min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolRunResponse(BaseModel):
    tool_name: str
    success: bool
    result: dict[str, Any]
    error: str | None = None


class ToolListResponse(BaseModel):
    tools: list[ToolMetadata]
