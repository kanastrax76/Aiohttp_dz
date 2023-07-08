from typing import Callable, Awaitable

from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware
from sqlalchemy import select

from middleware import session_middleware, auth_middleware
from models import User, get_engine, init_db
from validate import CreateUserSchema, validate, check_password, raise_http_error
from views import UserView, AdvertisementView, login, logout


async def app_context(app: web.Application):
    print("START")
    async with get_engine().begin() as conn:
        await init_db(conn)
    yield
    await get_engine().dispose()
    print("SHUTDOWN")


async def get_app():
    app = web.Application(middlewares=[session_middleware])
    app_auth_required = web.Application(middlewares=[session_middleware, auth_middleware])

    app.cleanup_ctx.append(app_context)

    app.add_routes(
        [
            web.post("/login", login),
            web.get("/logout", logout)
        ]
    )

    app.add_routes(
        [
            web.get("/users/{user_id:\d+}", UserView),
            web.post("/users/", UserView),
        ]
    )

    app_auth_required.add_routes(
        [
            web.get("/{adv_id:\d+}", AdvertisementView),
            web.post("", AdvertisementView),
            web.patch("/{adv_id:\d+}", AdvertisementView),
            web.delete("/{adv_id:\d+}", AdvertisementView),
        ]
    )

    app.add_subapp(prefix="/advs", subapp=app_auth_required)
    return app


if __name__ == '__main__':
    web.run_app(get_app())
