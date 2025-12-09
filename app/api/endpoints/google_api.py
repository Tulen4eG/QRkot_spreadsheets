from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, create_spreadsheets, update_spreadsheets_value
)


router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        wrapper_services: Aiogoogle = Depends(get_service),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создание таблицы с данными по закрытым благотворительным проектам.
    Доступно только для суперпользователя.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await update_spreadsheets_value(spreadsheet_id, projects, wrapper_services)
    url = "https://docs.google.com/spreadsheets/d/" + spreadsheet_id
    return {"Table url": url}
