from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

ROW_COUNT = 100
COLUMN_COUNT = 100
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
GOOGLE_TABLE_BODY = dict(
    properties=dict(
        title='Отчет за {date_time_now}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)


async def create_spreadsheets(
        wrapper_services: Aiogoogle
) -> str:
    """Создание таблицы."""
    date_time_now = datetime.now().strftime(DATE_FORMAT)
    spreadsheet_body = deepcopy(GOOGLE_TABLE_BODY)
    spreadsheet_body['properties']['title'] = (
        GOOGLE_TABLE_BODY['properties']['title'].format(
            date_time_now=date_time_now
        ))

    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=dict(
                type='user',
                role='writer',
                emailAddress=settings.email,
            ),
            fields='id'
        )
    )


async def update_spreadsheets_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(DATE_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in projects:
        new_row = [str(project[0]), str(project[1]), str(project[2])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
