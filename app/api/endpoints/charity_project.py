from fastapi import APIRouter, Depends
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_before_delete,
    check_charity_project_before_edit,
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investment import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, str]:
    '''
    Создание благотворительного проекта.
    Доступно только для суперпользователя.
    '''
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session, commit=False
    )
    session.add_all(invest(
        new_project,
        await donation_crud.get_not_fully_invested(session)
    ))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, str]:
    '''Получение списка всех благотворительных проектов.'''
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> Dict[str, str]:
    '''
    Редактирование благотворительного проекта.
    Доступно только для суперпользователя.
    '''
    return await charity_project_crud.update(
        await check_charity_project_before_edit(project_id, obj_in, session),
        obj_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, str]:
    '''
    Удаление благотворительного проекта.
    Доступно только для суперпользователя.
    '''
    return await charity_project_crud.remove(
        await check_charity_project_before_delete(project_id, session), session
    )
