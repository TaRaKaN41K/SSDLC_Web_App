import pytest
from unittest.mock import MagicMock
from fastapi import Request
from starlette.datastructures import Headers

from api.utils.client import get_device_id
from exceptions.custom_exceptions import ClienteIdentificationError


@pytest.mark.asyncio
async def test_get_device_id_normal_case():
    request = MagicMock(spec=Request)
    request.headers = Headers({"user-agent": "TestBrowser/1.0"})
    request.client = MagicMock()
    request.client.host = "127.0.0.1"

    device_id = await get_device_id(request)
    assert device_id == "127.0.0.1_TestBrowser/1.0"


@pytest.mark.asyncio
async def test_get_device_id_missing_ip():
    request = MagicMock(spec=Request)
    request.headers = Headers({"user-agent": "TestBrowser/2.0"})
    request.client = None

    device_id = await get_device_id(request)
    assert device_id == "unknown_ip_TestBrowser/2.0"


@pytest.mark.asyncio
async def test_get_device_id_missing_user_agent():
    request = MagicMock(spec=Request)
    request.headers = Headers({})
    request.client = MagicMock()
    request.client.host = "192.168.0.1"

    device_id = await get_device_id(request)
    assert device_id == "192.168.0.1_unknown"


@pytest.mark.asyncio
async def test_get_device_id_missing_all():
    request = MagicMock(spec=Request)
    request.headers = Headers({})
    request.client = None

    with pytest.raises(ClienteIdentificationError) as exc_info:
        await get_device_id(request)
    assert "Missing IP and User-Agent" in str(exc_info.value)
