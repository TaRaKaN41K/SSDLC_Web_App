from fastapi import FastAPI
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

from api.route import auth, user
from exceptions import app_http_exception_handler
from exceptions.custom_exceptions import BaseAppException
from config import UPLOAD_DIR

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(debug=True, title='Web_APP')

app.add_exception_handler(BaseAppException, app_http_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['Auth'])
app.include_router(user.router, tags=['User'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=False)
