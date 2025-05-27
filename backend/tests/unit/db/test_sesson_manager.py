import pytest
from unittest.mock import patch, AsyncMock
from db.session_manager import DatabaseSessionManager


@patch("db.session_manager.create_async_engine")
@patch("db.session_manager.async_sessionmaker")
def test_database_session_manager_init(mock_async_sessionmaker, mock_create_engine):
    mock_engine = mock_create_engine.return_value

    manager = DatabaseSessionManager()

    mock_create_engine.assert_called_once()
    mock_async_sessionmaker.assert_called_once_with(bind=mock_engine, expire_on_commit=False)

    assert manager.engine == mock_engine
    assert manager.async_session_maker == mock_async_sessionmaker.return_value

@pytest.mark.asyncio
@patch("db.session_manager.create_async_engine")
async def test_close_calls_dispose(mock_create_engine):
    manager = DatabaseSessionManager()
    manager.engine.dispose = AsyncMock()

    await manager.close()

    manager.engine.dispose.assert_awaited_once()
