from fastapi import APIRouter, FastAPI

from src.middlewares import ProcessTimeMiddleware
from src.users.router import user_notification_router, user_router


def create_app() -> FastAPI:
    app = FastAPI(title="Trading App")

    main_api_router = APIRouter()

    main_api_router.include_router(user_router, prefix="/users", tags=["User"])
    main_api_router.include_router(user_notification_router, prefix="/users", tags=["User Notification"])
    app.include_router(main_api_router)
    app.add_middleware(ProcessTimeMiddleware, some_attribute="foo")

    return app


app = create_app()
