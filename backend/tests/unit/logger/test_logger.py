import logging
import os
from unittest.mock import patch, MagicMock

from logger.logger import AppLogger


@patch("logger.logger.RotatingFileHandler")
@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
@patch("logging.getLogger")
def test_logger_creation(mock_get_logger, mock_exists, mock_makedirs, mock_rotating_handler):
    mock_logger = MagicMock()
    mock_logger.handlers = []
    mock_get_logger.return_value = mock_logger

    mock_handler_instance = MagicMock()
    mock_rotating_handler.return_value = mock_handler_instance

    log_file = "/tmp/logs/app.log"
    category = "testcat"
    level = logging.INFO

    app_logger = AppLogger(log_file=log_file, category=category, level=level)

    mock_get_logger.assert_called_once_with(f"app.{category}")
    mock_logger.setLevel.assert_called_once_with(level)
    mock_exists.assert_called_once_with(os.path.dirname(log_file))
    mock_makedirs.assert_called_once_with(os.path.dirname(log_file), exist_ok=True)
    mock_logger.addHandler.assert_called_once_with(mock_handler_instance)
    # Проверяем, что установился форматтер у мокированного handler
    mock_handler_instance.setFormatter.assert_called_once()
    formatter_arg = mock_handler_instance.setFormatter.call_args[0][0]
    assert isinstance(formatter_arg, logging.Formatter)
    assert "%(asctime)s" in formatter_arg._fmt


@patch("logger.logger.RotatingFileHandler")
@patch("os.makedirs")
@patch("os.path.exists", return_value=True)
@patch("logging.getLogger")
def test_logger_no_makedirs_if_dir_exists(mock_get_logger, mock_exists, mock_makedirs, mock_rotating_handler):
    mock_logger = MagicMock()
    mock_logger.handlers = []
    mock_get_logger.return_value = mock_logger

    mock_handler_instance = MagicMock()
    mock_rotating_handler.return_value = mock_handler_instance

    log_file = "/tmp/existing_dir/app.log"
    category = "cat2"

    AppLogger(log_file=log_file, category=category)

    mock_exists.assert_called_once_with(os.path.dirname(log_file))
    mock_makedirs.assert_not_called()
    mock_logger.addHandler.assert_called_once_with(mock_handler_instance)


@patch("logging.getLogger")
def test_logger_does_not_add_duplicate_handlers(mock_get_logger):
    mock_logger = MagicMock()
    mock_logger.handlers = [MagicMock()]
    mock_get_logger.return_value = mock_logger

    log_file = "/tmp/logs/app.log"
    category = "test"

    AppLogger(log_file=log_file, category=category)

    mock_logger.addHandler.assert_not_called()
