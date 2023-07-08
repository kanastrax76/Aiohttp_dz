import json
from datetime import datetime
from typing import Type, Optional

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from pydantic import BaseModel, EmailStr, ValidationError, ArbitraryTypeError
import bcrypt


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class CreateAdvSchema(BaseModel):
    title:  str
    description: str
    user_id: int


SCHEMA_TYPE = Type[CreateUserSchema] | Type[CreateAdvSchema]

ERROR_TYPE = Type[web.HTTPBadRequest] | Type[web.HTTPForbidden] \
             | Type[web.HTTPUnauthorized] | Type[web.HTTPNotFound] | Type[web.HTTPConflict]


def raise_http_error(error_class: ERROR_TYPE, message: str | dict):
    raise error_class(
        text=json.dumps({"status": error_class.status_code, "description": message}),
        content_type="application/json",
    )


async def validate(data: dict, schema: SCHEMA_TYPE) -> dict:
    try:
        validated = schema(**data)
    except ValidationError as error:
        raise raise_http_error(web.HTTPBadRequest, 'wrong data')
    return validated.dict()


def hash_password(password: str) -> str:
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode()


def check_password(
    password_hash: str,
    password: str,
) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
