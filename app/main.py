from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.config import Settings, Config
from app.clients.postgres import PostgresClient

from fastapi.middleware.cors import CORSMiddleware

from app.routers import router


config: Settings = Config.get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await PostgresClient.init_engine(config=config)
    yield
    await PostgresClient.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.docs_url = "/docs" if config.app.DEBUG is True else None
    app.redoc_url = "/redoc" if config.app.DEBUG is True else None
    app.swagger_ui_parameters = {"displayRequestDuration": config.app.DEBUG}

    app.include_router(router)

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
