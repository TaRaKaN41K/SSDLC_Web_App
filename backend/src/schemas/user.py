from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str
    password: bytes
    email: str
    photo_filename: str | None
    active: bool = True
