from fastapi import status
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    code: int = status.HTTP_200_OK
    data: Optional[T] = None
    msg: str = "success"

    class Config:
        json_encoders = {"datetime": lambda v: v.isoformat()}

class ErrorResponse(BaseModel):
    code: int = status.HTTP_400_BAD_REQUEST
    data: Optional[dict] = None
    msg: str = "error"
