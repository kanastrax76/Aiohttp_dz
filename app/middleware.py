from typing import Callable, Awaitable
from aiohttp import web, BasicAuth, FormData
from aiohttp.web_response import Response

from app.models import get_session_maker, get_engine, init_db, User
from validate import raise_http_error

Session = get_session_maker()


class CurrentUser(web.Request):
    user = None

    def login_user(self, user_id=None):
        self.user = user_id


@web.middleware
async def session_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    async with Session() as session:
        request["session"] = session
        return await handler(request)


@web.middleware
async def auth_middleware(
        request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> Awaitable[Response]:
    resp = await handler(request)
    current = FormData.current_user
    # us = request.headers.get('auth')
    # if not request.get('current_user'):
    return handler(request)
    raise raise_http_error(web.HTTPUnauthorized, {'status': 'Not authenticated'})
