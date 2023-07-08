from typing import Callable, Awaitable

from aiohttp import web, BasicAuth, FormData
from aiohttp_basicauth import BasicAuthMiddleware
from sqlalchemy import select

from crud import get_item, create_item, patch_item, delete_item
from middleware import CurrentUser
from models import User, Advertisement
from validate import validate, hash_password, CreateUserSchema, raise_http_error, check_password, CreateAdvSchema


async def login(request: web.Request):
    login_data = await request.json()
    login_data = await validate(login_data, CreateUserSchema)
    result = await request['session'].execute(select(User).where(User.email == login_data['email']))
    user = result.scalar()
    if user.email == login_data['email'] and check_password(user.password, login_data['password']):
        # auth = BasicAuth(login=user.email, password=user.password, encoding='utf-8')
        auth = FormData()
        auth.add_field('current_user', user.id)
        # current_user = CurrentUser()
        # current_user.login_user(user.id)
        # request['auth'] = auth


        return auth # web.json_response({'status': 'Auth is successfully'})
    raise raise_http_error(web.HTTPUnauthorized, {'status': 'Not authenticated'})


async def logout(request: web.Request):
    request['current_user'] = None
    # current_user.login_user(user_id=None)
    return web.json_response({'status': 'Auth logout'})


class UserView(web.View):
    async def post(self):
        user_data = await self.request.json()
        user_data = await validate(user_data, CreateUserSchema)
        user_data['password'] = hash_password(user_data['password'])
        new_user = await create_item(self.request['session'], User, **user_data)
        # auth = LoginUser(request, handler)
        return web.json_response(
            {
                'id': new_user.id,
                'email': new_user.email
            }
        )

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_item(self.request['session'], User, user_id)
        if user is None:
            raise raise_http_error(web.HTTPNotFound, f"User id {user_id} not found")
        return web.json_response(
            {
                'id': user.id,
                'email': user.email
            }
        )


class AdvertisementView(web.View):
    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await get_item(self.request['session'], Advertisement, adv_id)
        if adv is None:
            raise raise_http_error(web.HTTPNotFound, f"Advertisement id {adv_id} not found")
        return web.json_response(
            {
                'id': adv.id,
                'title': adv.title,
                'description': adv.description,
                'user_id': adv.user_id,
                'created_at': str(adv.created_at)
            }
        )

    # @app.required
    async def post(self):
        adv_data = await self.request.json()
        adv_data['user_id'] = self.request['current_user']
        adv_data = await validate(adv_data, CreateAdvSchema)
        new_adv = await create_item(self.request['session'], Advertisement, **adv_data)
        return web.json_response(
            {
                'id': new_adv.id,
                'title': new_adv.title,
                'description': new_adv.description,
                'user_id': new_adv.user_id,
                # 'created_at': str(new_adv.created_at)
            }
        )

    async def patch(self):
        patch_id = int(self.request.match_info['adv_id'])
        patch_data = await self.request.json()
        patch_data = await validate(patch_data, CreateAdvSchema)
        patch_adv = await get_item(self.request['session'], Advertisement, patch_id)
        patched = await patch_item(self.request['session'], patch_adv, **patch_data)
        if patched is None:
            raise raise_http_error(web.HTTPNotFound, f"Advertisement id {patch_id} not found")
        return web.json_response(
            {
                'id': patched.id,
                'title': patched.title,
                'description': patched.description,
                'user_id': patched.user_id,
                'created_at': str(patched.created_at)
            }
        )

    async def delete(self) -> dict:
        delete_id = int(self.request.match_info['adv_id'])
        delete_adv = await get_item(self.request['session'], Advertisement, delete_id)
        deleted = await delete_item(self.request['session'], delete_adv)
        return deleted
