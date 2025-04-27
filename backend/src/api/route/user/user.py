from fastapi import APIRouter, Depends

from .endpoints import (
    create_account,
    delete_account,
    edit_profile,
    get_all_users,
    me
)
from config import http_bearer


router = APIRouter(
    prefix="/user",
)

router.add_api_route(
    path='/me',
    endpoint=me,
    methods=["GET"],
    dependencies=[Depends(http_bearer)]
)

router.add_api_route(
    path='/get_all_users',
    endpoint=get_all_users,
    methods=["GET"],
)

router.add_api_route(
    path='/create_account',
    endpoint=create_account,
    methods=["POST"])

router.add_api_route(
    path='/edit_profile',
    endpoint=edit_profile,
    methods=["POST"],
    dependencies=[Depends(http_bearer)]
)

router.add_api_route(
    path='/delete_account',
    endpoint=delete_account,
    methods=["DELETE"],
    dependencies=[Depends(http_bearer)]
)
