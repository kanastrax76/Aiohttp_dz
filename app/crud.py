from aiohttp import web
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from middleware import Session
from validate import raise_http_error
from models import ORM_MODEL, ORM_MODEL_CLS


async def get_item(session: Session, model_cls: ORM_MODEL_CLS, item_id: int) -> ORM_MODEL:
    item = await session.get(model_cls, item_id)
    if item is None:
        raise raise_http_error(web.HTTPNotFound, f"{model_cls.__name__.lower()} not found")
    return item


async def create_item(session: Session, model_cls: ORM_MODEL_CLS, commit: bool = True, **params) -> ORM_MODEL:
    new_item = model_cls(**params)
    session.add(new_item)
    if commit:
        try:
            await session.commit()
        except IntegrityError as er:
            if er.code == 'gkpj':
                raise raise_http_error(web.HTTPConflict, f"such {model_cls.__name__.lower()} already exists")
    return new_item


async def patch_item(session: Session, item: ORM_MODEL, commit: bool = True, **params) -> ORM_MODEL:
    for field, value in params.items():
        setattr(item, field, value)
    session.add(item)
    if commit:
        try:
            await session.commit()
        except IntegrityError as er:
            if er.code == 'gkpj':
                raise raise_http_error(409, f"attr already exists")
    return item


async def delete_item(session: Session, item: ORM_MODEL, commit: bool = True) -> dict:
    await session.delete(item)
    if commit:
        await session.commit()
        return {"status": "deleted"}
