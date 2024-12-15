import logging

from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repositories.users import UserRepository
from src.schemas import UserCreate

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        avatar = None
        try:
            gravatar_inst = Gravatar(body.email)
            avatar = gravatar_inst.get_image()
        except Exception as e:
            logger.error("Create user exception occurred: %s", e)

        return await self.repository.create_user(body, avatar)
    
    async def get_user_by_username(self, username: str):
        return await self.repository.get_user_by_username(username)

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def update_avatar_url(self, email: str, url: str):
        return await self.repository.update_avatar_url(email, url)
    
    async def confirmed_email(self, email: str):
        return await self.repository.confirm_email(email)