from db.session_manager import db_manager
from logger import loggers


def connection(method):
    async def wrapper(*args, **kwargs):
        async with db_manager.async_session_maker() as session:
            try:
                result = await method(*args, session=session, **kwargs)
                loggers['db'].info(f"Успешное выполнение метода {method.__name__}")
                return result
            except Exception as e:
                await session.rollback()
                loggers['db'].error(f"Ошибка при выполнении метода {method.__name__}: {str(e)}")
                raise e
            finally:
                await session.close()
                loggers['db'].info(f"Сессия для метода {method.__name__} закрыта.")
    return wrapper
