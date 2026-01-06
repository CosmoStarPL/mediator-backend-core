from fastapi import APIRouter
from src.schemas import CreateModel, Model, ActionModel, CopyModel
from src.requests.OllamaClient import OllamaAsyncClient

router = APIRouter(
    prefix="/op",
    tags=["Op"]
)


@router.post("/models/create")
async def create_model(body: CreateModel):
    async with OllamaAsyncClient() as client:
        return await client.create_model(body)


@router.delete("/models/delete")
async def delete_model(body: Model):
    async with OllamaAsyncClient() as client:
        return await client.delete_model(body)


@router.post("/models/pull")
async def pull_model(body: ActionModel):
    async with OllamaAsyncClient() as client:
        return await client.pull_model(body)


@router.post("/models/push")
async def push_model(body: ActionModel):
    async with OllamaAsyncClient() as client:
        return await client.push_model(body)


@router.post("/models/copy")
async def copy_model(body: CopyModel):
    async with OllamaAsyncClient() as client:
        return await client.copy_model(body)
