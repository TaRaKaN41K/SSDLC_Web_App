from fastapi import Request

from exceptions.custom_exceptions import ClienteIdentificationError


async def get_device_id(request: Request) -> str:
    user_agent = request.headers.get("user-agent", "unknown")
    ip_address = request.client.host if request.client else "unknown_ip"

    if ip_address == "unknown_ip" and user_agent == "unknown":
        raise ClienteIdentificationError("Missing IP and User-Agent in request")

    device_id = f"{ip_address}_{user_agent}"
    return device_id

