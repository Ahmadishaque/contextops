from fastapi import APIRouter

from app.schemas.tool import ToolListResponse, ToolRunRequest, ToolRunResponse
from app.services.tools.registry import get_tool_registry

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=ToolListResponse)
def list_tools() -> ToolListResponse:
    registry = get_tool_registry()
    return ToolListResponse(tools=registry.list_tools())


@router.post("/run", response_model=ToolRunResponse)
def run_tool(request: ToolRunRequest) -> ToolRunResponse:
    registry = get_tool_registry()

    try:
        result = registry.run_tool(
            tool_name=request.tool_name,
            arguments=request.arguments,
        )
        return ToolRunResponse(
            tool_name=request.tool_name,
            success=True,
            result=result,
            error=None,
        )
    except Exception as exc:
        return ToolRunResponse(
            tool_name=request.tool_name,
            success=False,
            result={},
            error=str(exc),
        )
