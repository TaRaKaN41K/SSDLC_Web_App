import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class AsyncContextManagerMock:
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.mark.asyncio
async def test_connection_success():
    mock_method = AsyncMock(return_value="result")
    mock_method.__name__ = "mock_method"  # добавлено

    mock_session = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()

    mock_async_session_maker = MagicMock(
        return_value=AsyncContextManagerMock(mock_session))

    mock_logger = MagicMock()
    with patch("db.session_manager.db_manager.async_session_maker",
               mock_async_session_maker), \
            patch("db.connection_decorator.loggers", {"db": mock_logger}):
        from db.connection_decorator import connection
        decorated = connection(mock_method)
        result = await decorated()

        assert result == "result"
        mock_method.assert_awaited_once()
        mock_logger.info.assert_any_call(
            "Успешное выполнение метода mock_method")
        mock_logger.info.assert_any_call(
            "Сессия для метода mock_method закрыта.")
        mock_session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_connection_failure():
    error = Exception("fail")
    mock_method = AsyncMock(side_effect=error)

    mock_session = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()

    mock_async_session_maker = MagicMock(
        return_value=AsyncContextManagerMock(mock_session))

    mock_logger = MagicMock()
    with patch("db.session_manager.db_manager.async_session_maker",
               mock_async_session_maker), \
            patch("db.connection_decorator.loggers", {"db": mock_logger}):
        from db.connection_decorator import connection
        decorated = connection(mock_method)

        with pytest.raises(Exception) as exc:
            await decorated()

        assert exc.value == error
        mock_logger.error.assert_called_once()
        mock_session.rollback.assert_awaited_once()
        mock_session.close.assert_awaited_once()
