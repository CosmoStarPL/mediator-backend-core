import os
import httpx
from typing import Any, Dict, Optional
from src.schemas import GenerateText, Embedding


class OllamaAsyncClient:
    def __init__(self, base_url: Optional[str] = None, timeout: float = 10.0):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.client = httpx.AsyncClient(
            base_url=f"{self.base_url}/api",
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = await self.client.request(method, endpoint, params=params, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"status": "error", "code": e.response.status_code, "detail": e.response.text}
        except httpx.RequestError as e:
            return {"status": "error", "message": str(e)}

    # --- API Methods ---

    async def get_models(self) -> Dict[str, Any]:
        return await self._request("GET", "/tags")

    async def get_running_models(self) -> Dict[str, Any]:
        return await self._request("GET", "/ps")

    async def get_version(self) -> Dict[str, Any]:
        return await self._request("GET", "/version")

    async def get_model_info(self, model: str):
        return await self._request("POST", "/show", json={"model": model})

    async def generate(self, request_body: GenerateText):
        return await self._request("POST", "/generate", json=request_body.model_dump())

    async def generate_embeddings(self, request_body: Embedding):
        return await self._request("POST", "/embed", json=request_body.model_dump())
