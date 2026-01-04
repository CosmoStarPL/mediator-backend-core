from pydantic import BaseModel

class ModelOptions(BaseModel):
    temperature: float = 0.5
    stop: str = None
    num_predict: int = None

class Embedding(BaseModel):
    model: str
    input: str
    truncate: bool = True
    dimensions: int = None
    options: ModelOptions = None
