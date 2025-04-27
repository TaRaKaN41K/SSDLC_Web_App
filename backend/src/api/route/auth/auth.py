from fastapi import APIRouter, Depends

from .endpoints import login, logout, regenerate_access
from config import http_bearer


router = APIRouter(
    prefix="/auth",
)

router.add_api_route(
    path='/login',
    endpoint=login,
    methods=["POST"])

router.add_api_route(
    path='/regenerate_access',
    endpoint=regenerate_access,
    methods=["POST"],
    dependencies=[Depends(http_bearer)]
)

router.add_api_route(
    path='/logout',
    endpoint=logout,
    methods=["GET"],
    dependencies=[Depends(http_bearer)]
)
