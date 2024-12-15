from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Contact
from src.schemas import ContactModel


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self._db_session = session

    async def get_contacts(
        self, first_name: str, last_name: str, email: str, skip: int, limit: int
    ) -> List[Contact]:
        query = (
            select(Contact)
            .where(Contact.first_name.contains(first_name))
            .where(Contact.last_name.contains(last_name))
            .where(Contact.email.contains(email))
            .offset(skip)
            .limit(limit)
        )
        result = await self._db_session.execute(query)
        return list(result.scalars().all())

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        query = select(Contact).filter_by(id=contact_id)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        new_contact = Contact(**body.model_dump(exclude_unset=True))
        self._db_session.add(new_contact)
        await self._db_session.commit()
        await self._db_session.refresh(new_contact)
        return new_contact

    async def update_contact(self, contact_id: int, body: ContactModel) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if not contact:
            return None
        update_data = body.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(contact, field, value)
        await self._db_session.commit()
        await self._db_session.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self._db_session.delete(contact)
            await self._db_session.commit()
        return contact

    async def does_contact_exist(self, email: str, phone_number: str) -> bool:
        query = select(Contact).where(
            or_(Contact.email == email, Contact.phone_number == phone_number)
        )
        result = await self._db_session.execute(query)
        return result.scalars().first() is not None

    async def get_upcoming_birthdays(self, days: int) -> List[Contact]:
        today = date.today()
        end_date = today + timedelta(days=days)

        query = (
            select(Contact)
            .where(
                or_(
                    func.date_part("day", Contact.birthday_date).between(
                        func.date_part("day", today), func.date_part("day", end_date)
                    ),
                    and_(
                        func.date_part("day", end_date) < func.date_part("day", today),
                        or_(
                            func.date_part("day", Contact.birthday_date) >= func.date_part("day", today),
                            func.date_part("day", Contact.birthday_date) <= func.date_part("day", end_date),
                        ),
                    ),
                )
            )
            .order_by(func.date_part("day", Contact.birthday_date).asc())
        )

        result = await self._db_session.execute(query)
        return list(result.scalars().all())