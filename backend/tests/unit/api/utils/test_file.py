import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from api.utils.file import upload_photo, delete_photo_file
from exceptions.custom_exceptions import InvalidFileExtensionError, \
    FileUploadError, FileDeletionError
from fastapi import UploadFile


# Создаем мок, который поддерживает async context manager
class AsyncContextManagerMock:
    def __init__(self, mock_obj):
        self.mock_obj = mock_obj

    async def __aenter__(self):
        return self.mock_obj

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.mark.asyncio
async def test_upload_photo_success(tmp_path):
    photo_file = AsyncMock(spec=UploadFile)
    photo_file.filename = "test.jpg"
    photo_file.read = AsyncMock(side_effect=[b"filecontent", b""])
    photo_file.seek = AsyncMock()

    mock_file = AsyncMock()

    with patch("api.utils.file.os.path.splitext", return_value=("test", ".jpg")), \
         patch("api.utils.file.uuid.uuid4", return_value="uuid1234"), \
         patch("api.utils.file.os.path.join", return_value=str(tmp_path / "uuid1234.jpg")), \
         patch("api.utils.file.aiofiles.open", return_value=AsyncContextManagerMock(mock_file)), \
         patch("api.utils.file.loggers", {"utils": MagicMock()}):

        filename_result = await upload_photo(photo_file)

        assert filename_result == "uuid1234.jpg"
        photo_file.read.assert_called()
        photo_file.seek.assert_called_once()
        mock_file.write.assert_called()


@pytest.mark.asyncio
async def test_upload_photo_invalid_extension():
    photo_file = AsyncMock(spec=UploadFile)
    photo_file.filename = "test.txt"  # расширение не из ALLOWED_EXTENSIONS

    with patch("api.utils.file.os.path.splitext", return_value=("test", ".txt")), \
            patch("api.utils.file.ALLOWED_EXTENSIONS", {".jpg", ".png"}):
        with pytest.raises(InvalidFileExtensionError):
            await upload_photo(photo_file)


@pytest.mark.asyncio
async def test_upload_photo_write_error(monkeypatch):
    photo_file = AsyncMock()
    photo_file.filename = "test.jpg"
    photo_file.read = AsyncMock(side_effect=[b"data", b""])
    photo_file.seek = AsyncMock()

    mock_buffer = AsyncMock()
    mock_buffer.write.side_effect = Exception("Write error")

    async_cm = AsyncContextManagerMock(mock_buffer)
    monkeypatch.setattr("api.utils.file.aiofiles.open", lambda *args, **kwargs: async_cm)

    from api.utils.file import upload_photo

    with pytest.raises(Exception) as exc_info:
        await upload_photo(photo_file)

    assert "Write error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_photo_file_success(tmp_path):
    filename = "file_to_delete.jpg"
    file_path = tmp_path / filename

    with patch("api.utils.file.os.path.join", return_value=str(file_path)), \
            patch("api.utils.file.aiofiles.os.path.exists",
                  AsyncMock(return_value=True)), \
            patch("api.utils.file.aiofiles.os.remove", AsyncMock()) as mock_remove, \
            patch("api.utils.file.loggers", {"utils": MagicMock()}):
        result = await delete_photo_file(filename)
        assert result is True
        mock_remove.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_photo_file_empty_name():
    result = await delete_photo_file("")
    assert result is True


@pytest.mark.asyncio
async def test_delete_photo_file_not_found():
    with patch("api.utils.file.aiofiles.os.path.exists",
               AsyncMock(return_value=False)):
        with pytest.raises(FileDeletionError):
            await delete_photo_file("nonexistent.jpg")


@pytest.mark.asyncio
async def test_delete_photo_file_remove_error():
    with patch("api.utils.file.aiofiles.os.path.exists",
               AsyncMock(return_value=True)), \
            patch("api.utils.file.aiofiles.os.remove",
                  AsyncMock(side_effect=Exception("remove failed"))):
        with pytest.raises(FileDeletionError):
            await delete_photo_file("somefile.jpg")
