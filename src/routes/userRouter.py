from fastapi import APIRouter
from src.requests.OllamaClient import OllamaAsyncClient
from src.schemas import GenerateText

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/chat")
async def start_chat(body: GenerateText):
    async with OllamaAsyncClient() as client:
        return await client.generate(body)

@router.get("/models")
async def show_running_models():
    async with OllamaAsyncClient() as client:
        return await client.get_running_models()

@router.get("/info/{model_name}")
async def model_info(model_name: str):
    async with OllamaAsyncClient() as client:
        return await client.get_model_info(model_name)
