from pydantic import BaseModel
class ModelOptions(BaseModel):
    temperature: float = 0.5
    stop: str = None
    num_predict: int = None

class GenerateText(BaseModel):
    role: str
    client: str
    prompt: str
    model: str
    format: bool = None
    stream: bool = False
    system: str = None
    raw: bool = False
    options: ModelOptions = None
