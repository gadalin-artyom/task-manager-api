from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(
        title="Task Manager API",
        version="1.0.0",
    )

    app.include_router(api_router, prefix="/api/v1")

    Instrumentator().instrument(app).expose(app)

    return app


app = get_application()
