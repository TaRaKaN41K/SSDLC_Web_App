from fastapi import UploadFile
import os
import aiofiles.os
import uuid

from config import UPLOAD_DIR, ALLOWED_EXTENSIONS
from logger import loggers
from exceptions.custom_exceptions import (
    InvalidFileExtensionError,
    FileUploadError,
    FileDeletionError
)


async def upload_photo(photo_file: UploadFile) -> str:
    _, file_extension = os.path.splitext(photo_file.filename or "")
    new_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, new_filename)

    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise InvalidFileExtensionError(f"Недопустимый формат файла: {file_extension}")
    try:

        async with aiofiles.open(file_location, 'wb') as buffer:
            while chunk := await photo_file.read(1024 * 1024):
                await buffer.write(chunk)

        await photo_file.seek(0)

        loggers['utils'].info(f"Файл успешно загружен: {new_filename}")
        return new_filename

    except Exception as e:
        if os.path.exists(file_location):
            try:
                await aiofiles.os.remove(file_location)
                loggers['utils'].info(
                    f"Неудачно загруженный файл удален: {file_location}")
            except Exception as cleanup_error:
                loggers['utils'].exception(
                    f"Ошибка при удалении поврежденного файла: {str(cleanup_error)}")
                raise FileUploadError(
                    f"Ошибка при удалении поврежденного файла: {str(cleanup_error)}")

        raise FileUploadError(f"Не удалось загрузить файл: {str(e)}")


async def delete_photo_file(photo_filename: str) -> bool:
    if not photo_filename:
        loggers['utils'].info("Удаление не требуется: имя файла пустое")
        return True

    file_location = os.path.join(UPLOAD_DIR, photo_filename)

    if not await aiofiles.os.path.exists(file_location):
        raise FileDeletionError(f"Файл для удаления не найден: {file_location}")

    try:
        await aiofiles.os.remove(file_location)
        loggers['utils'].info(f"Файл успешно удалён: {file_location}")
        return True
    except Exception as e:
        raise FileDeletionError(f"Не удалось удалить файл: {str(e)}")
