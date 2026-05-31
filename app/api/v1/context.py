from fastapi import APIRouter

from app.schemas.context import ContextAssembleRequest, ContextAssembleResponse
from app.services.context.assembler import ContextAssembler

router = APIRouter(prefix="/context", tags=["context"])


@router.post("/assemble", response_model=ContextAssembleResponse)
def assemble_context(request: ContextAssembleRequest) -> ContextAssembleResponse:
    assembler = ContextAssembler()
    context_package = assembler.assemble(request)

    return ContextAssembleResponse(context_package=context_package)
