
from typing import Sequence

from app.db.models.user import User
from app.schemas.user_schemas import UserGetSchema, UserPostSchema
from app.utils.logger import log
from app.utils.repository_transaction_managaer import \
    AbstractRepositoryTransactionManagaer


class UserService():
    def __init__(self, repository_manager: AbstractRepositoryTransactionManagaer):
        self.repository_manager = repository_manager

    @staticmethod 
    async def insert(repository_manager: AbstractRepositoryTransactionManagaer, user_post: UserPostSchema) -> int | None:
        async with repository_manager:
            try:
                user_id: int | None = await repository_manager.user_repo.insert(user_post.model_dump())
                await repository_manager.commit()
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None

            return user_id

    @staticmethod
    async def find_one(repository_manager: AbstractRepositoryTransactionManagaer, **filters) -> UserGetSchema | None:
        async with repository_manager:
            try:
                user: User | None = await repository_manager.user_repo.find_one(filters)
                if not user:
                    return None 
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None
            
            return UserGetSchema(
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                mail=user.mail,
                tz=user.tz,
                id=user.id
            )

    @staticmethod 
    async def get_mail_id_mapping(repository_manager: AbstractRepositoryTransactionManagaer) -> dict[str, int] | None:
        async with repository_manager:
            mapping = {}
            try:
                users: Sequence[User] = await repository_manager.user_repo.get_all()
                if users == []:
                    return None
                for user in users:
                    mapping[user.mail] = user.id
            except Exception as e:
                log.error(f"Some error occurred while generate users mapping: {e}")
                return None
            
            return mapping