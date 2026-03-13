from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from src.api.v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_application(router: APIRouter) -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(router)
    return application


app = create_application(router=router)
