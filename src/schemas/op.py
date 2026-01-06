from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, Optional


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    role: Role
    content: str


class CreateModel(BaseModel):
    model: str
    create_from: Optional[str] = Field(default=None, alias="from")
    template: Optional[str] = None
    system: Optional[str] = None
    license: Optional[str] = None
    parameters: Optional[Dict[Any, Any]] = None
    message: Optional["Message"] = None
    stream: bool = True
    quantize: Optional[str] = None


class Model(BaseModel):
    model: str


class ActionModel(BaseModel):
    model: str
    insecure: Optional[bool] = None
    stream: bool = True


class CopyModel(BaseModel):
    source: str
    destination: str
