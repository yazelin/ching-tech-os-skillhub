"""SkillHub API server — minimal FastAPI application."""

from fastapi import FastAPI

from server.routes import router

app = FastAPI(
    title="SkillHub API",
    version="0.1.0",
    description="CTOS skill registry HTTP interface.",
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server.main:app", host="127.0.0.1", port=8787, reload=True)
