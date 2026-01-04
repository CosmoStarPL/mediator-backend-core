from fastapi import APIRouter
from src.requests.OllamaClient import OllamaAsyncClient
from src.schemas import Embedding

router = APIRouter(
    prefix="/dev",
    tags=["Dev"]
)

@router.post("/embed")
async def make_embeddings(body: Embedding):
    async with OllamaAsyncClient() as client:
        return await client.generate_embeddings(body)
