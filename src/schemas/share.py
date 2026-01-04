from enum import Enum
from pydantic import BaseModel
from typing import Dict, List

class Roles(Enum):
    USER = "USER"
    DEV = "DEV"
    OP = "OP"

class ModelOptions(BaseModel):
    temperature: float = 0.5
    stop: str = None
    num_predict: int = None

class _EndpointDoc(BaseModel):
    path: str
    method: str
    description: str

class APIInfo(BaseModel):
    greeting: str
    root_path: str
    docs_preview: Dict[str, List[_EndpointDoc]]
    telemetry: Dict[str, str]
    links: Dict[str, str]
