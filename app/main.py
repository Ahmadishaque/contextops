from fastapi import FastAPI

app = FastAPI(
    title="ContextOps",
    description="Production context engineering platform for tool-using AI agents.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "ContextOps API"}
