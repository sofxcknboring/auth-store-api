from fastapi_users import schemas
from pydantic import field_validator


class UserRead(schemas.BaseUser[int]):
    full_name: str
    phone: str


class UserCreate(schemas.BaseUserCreate):
    full_name: str
    phone: str

    @field_validator("phone")
    def validate_phone(cls, v):
        if not v.startswith("+7") or len(v) != 12 or not v[1:].isdigit():
            raise ValueError(
                "The phone number must start with +7 and contain 10 digits"
            )
        return v


class UserUpdate(schemas.BaseUserUpdate):
    full_name: str
    phone: str
