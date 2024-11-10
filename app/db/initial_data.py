from app.schemas.user_schemas import UserPostSchema
from app.services.priority_service import PriorityService
from app.services.status_service import StatusService
from app.services.system_service import SystemService
from app.services.user_service import UserService
from app.utils.repository_transaction_managaer import \
    SqlAlchemyRepositoryTransactionManagaer

STATUSES = ["Новый", "В работе", "Исполнено"]

PRIORITIES = ["Нормальный", "Критический"]

SYSYTEMS = ["mclim", "transformer", "amelia", "lift"]

ADMIN_USER = UserPostSchema(
    first_name="Александр",
    last_name="Пархоменко",
    middle_name="",
    mail="parkhomenko.av@dvfu.ru",
    tz="Asia/Vladivostok"
)


async def init_db(statuses=STATUSES, priorities=PRIORITIES, systems=SYSYTEMS):
    uow = SqlAlchemyRepositoryTransactionManagaer()
    
    if not await StatusService.find_one(uow, title=statuses[0]):
        await StatusService.bulk_insert(uow, statuses)
    
    if not await PriorityService.find_one(uow, title=priorities[0]):
        await PriorityService.bulk_insert(uow, priorities)

    if not await SystemService.find_one(uow, title=systems[0]):
        await SystemService.bulk_insert(uow, systems)   

    if not await UserService.find_one(uow, mail="parkhomenko.av@dvfu.ru"):
        await UserService.insert(uow, ADMIN_USER)
