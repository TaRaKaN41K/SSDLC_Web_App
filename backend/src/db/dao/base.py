from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional, Dict, Any

from ..connection_decorator import connection
from logger import loggers
from exceptions.custom_exceptions import (
    ModelNotDefinedError,
    UniqueConstraintViolationError,
    DatabaseError,
    UnexpectedError,
    RecordNotFoundError,
    FieldNotExistError
)


class BaseDAO:
    model = None

    @classmethod
    def _validate_model_defined(cls):
        if not hasattr(cls, "model") or cls.model is None:
            raise ModelNotDefinedError("Модель должна быть определена в подклассе!")

    @classmethod
    @connection
    async def add(cls, session: AsyncSession, **values):
        cls._validate_model_defined()

        try:
            new_instance = cls.model(**values)
            session.add(new_instance)
            await session.commit()
            await session.refresh(new_instance)
            loggers['db'].info(f"Создан новый объект: {new_instance}")
            return new_instance

        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e.orig)
            loggers['db'].error(f"Ошибка уникальности при добавлении: {error_msg}")
            if "users_name_key" in error_msg:
                raise UniqueConstraintViolationError("Username is already exist")
            elif "users_email_key" in error_msg:
                raise UniqueConstraintViolationError("Email is already exist")
            else:
                raise UniqueConstraintViolationError("Нарушение уникальности данных")

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Ошибка базы данных при добавлении: {str(e)}")
        except Exception as e:
            await session.rollback()
            raise UnexpectedError(f"Неожиданная ошибка при создании записи: {str(e)}")

    @classmethod
    @connection
    async def get_by_id(cls, session: AsyncSession, instance_id: int) -> Optional[Dict[str, Any]]:
        cls._validate_model_defined()

        try:
            instance = await session.get(cls.model, instance_id)
            if instance is None:
                raise RecordNotFoundError(f"Запись с id={instance_id} не найдена")
            loggers['db'].info(f"Получена запись по id={instance_id}")
            return instance
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка получения записи по id: {str(e)}")
        except Exception as e:
            raise UnexpectedError(f"Неожиданная ошибка при получении записи по id: {str(e)}")

    @classmethod
    @connection
    async def get_by_parameter(cls, session: AsyncSession, **filters):
        cls._validate_model_defined()

        try:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            instance = result.scalars().first()
            if instance is None:
                raise RecordNotFoundError(f"Нет записей по фильтрам: {filters}")
            loggers['db'].info(f"Получена запись по фильтрам: {filters}")
            return instance
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка запроса к базе данных: {str(e)}")
        except Exception as e:
            raise UnexpectedError(f"Неожиданная ошибка в запросе: {str(e)}")

    @classmethod
    @connection
    async def delete_by_parameter(cls, session: AsyncSession, **filters):
        cls._validate_model_defined()

        try:
            query = select(cls.model).filter_by(**filters)
            records_to_delete = (await session.scalars(query)).all()

            if not records_to_delete:
                raise RecordNotFoundError(f"Нет записей по фильтрам: {filters}")

            for record in records_to_delete:
                await session.delete(record)

            await session.commit()
            loggers['db'].info(f"Удалено записей: {len(records_to_delete)} по фильтрам: {filters}")
            return True

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Ошибка удаления записи: {str(e)}")

        except Exception as e:
            await session.rollback()
            raise UnexpectedError(f"Неожиданная ошибка при удалении: {str(e)}")

    @classmethod
    @connection
    async def delete_by_id(cls, session: AsyncSession, instance_id: int):
        cls._validate_model_defined()

        try:
            instance = await session.get(cls.model, instance_id)
            if instance is None:
                raise RecordNotFoundError(f"Удаление: запись с id={instance_id} не найдена")

            await session.delete(instance)
            await session.commit()
            loggers['db'].info(f"Удалена запись с id={instance_id}")
            return instance

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Ошибка удаления записи: {str(e)}")

        except Exception as e:
            await session.rollback()
            raise UnexpectedError(f"Неожиданная ошибка при удалении: {str(e)}")

    @classmethod
    @connection
    async def update_by_id(cls, session: AsyncSession, instance_id: int, **values) -> Dict[str, Any]:
        cls._validate_model_defined()

        try:
            instance = await session.get(cls.model, instance_id)
            if instance is None:
                raise RecordNotFoundError(f"Запись с id={instance_id} не найдена")

            for key, value in values.items():
                if not hasattr(instance, key):
                    raise FieldNotExistError(f"Поле {key} не существует в модели")
                setattr(instance, key, value)

            await session.commit()
            await session.refresh(instance)
            loggers['db'].info(f"Обновлена запись с id={instance_id}: {values}")
            return instance
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Ошибка обновления записи: {str(e)}")
        except Exception as e:
            await session.rollback()
            raise UnexpectedError(f"Неожиданная ошибка при обновлении: {str(e)}")

    @classmethod
    @connection
    async def get_all(
            cls,
            session: AsyncSession,
            page: int,
            limit: int
    ) -> List[Dict[str, Any]]:
        cls._validate_model_defined()

        try:
            skip = max((page - 1) * limit, 0)

            query = select(cls.model).offset(skip).limit(limit)
            result = await session.execute(query)

            instances = result.scalars().all()

            loggers['db'].info(f"Получены {len(instances)} записей (страница {page})")

            return [
                {k: v for k, v in instance.__dict__.items() if not k.startswith('_')}
                for instance in instances
            ]
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка получения записей: {str(e)}")
        except Exception as e:
            raise UnexpectedError(f"Неожиданная ошибка при получении записей: {str(e)}")

    @classmethod
    @connection
    async def count_all(cls, session: AsyncSession) -> int:
        try:
            query = select(func.count()).select_from(cls.model)
            result = await session.execute(query)
            total_users = result.scalar()
            return total_users
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка подсчета записей: {str(e)}")
        except Exception as e:
            raise UnexpectedError(f"Неожиданная ошибка при подсчете записей: {str(e)}")

