"""Application module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.init_resources()

    db = container.db()
    db.create_database()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.container = container
    app.include_router(endpoints.user_router)
    app.include_router(endpoints.order_router)

    @app.get("/status")
    def get_status():
        return {"status": "OK"}

    return app


app = create_app()
