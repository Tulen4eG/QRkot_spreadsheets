from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

PROJECT_NAME_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
CANT_DELETE_INVESTED_PROJECT = (
    'Нельзя удалить закрытый проект или проект, '
    'в который уже были инвестированы средства.'
)
CANT_EDIT_CLOSED_PROJECT = 'Нельзя вносить изменения в закрытый проект!'
FULL_AMOUNT_LESS_THAN_INVESTED = (
    'Нельзя установить значение full_amount меньше уже вложенной суммы.'
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    if await charity_project_crud.get_by_attribute(
        'name', project_name, session
    ) is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_EXISTS
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_charity_project_before_delete(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.invested_amount > 0 or charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANT_DELETE_INVESTED_PROJECT
        )
    return charity_project


async def check_charity_project_before_edit(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANT_EDIT_CLOSED_PROJECT
        )
    if obj_in.full_amount is not None:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=FULL_AMOUNT_LESS_THAN_INVESTED
            )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    return charity_project
