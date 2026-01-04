import time
import psutil
import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from src.router import router as main_router
import os
from src.middleware.api_keys import auth_check
from src.schemas import APIInfo

load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

app = FastAPI(root_path=ROOT_PATH)

# Routes
app.include_router(main_router)

# Uptime
START_TIME = time.time()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    return await auth_check(request=request, call_next=call_next)


@app.get("/who")
async def who(request: Request):
    return {
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "api_key": request.headers.get("authorization"),
        "cookies": request.cookies,
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
    }


@app.get("/", response_model=APIInfo)
async def root_greeting():
    return {
        "greeting": "Infrastructure Core API Node. Systems operational.",
        "root_path": os.getenv("ROOT_PATH"),
        "docs_preview": {
            "/user": [
                {
                    "path": "/chat",
                    "method": "POST",
                    "description": "Start a temporary chat"
                },
                {
                    "path": "/models",
                    "method": "GET",
                    "description": "Shows active models"
                },
                {
                    "path": "/info",
                    "method": "POST",
                    "description": "Gives detailed information about a model"
                }
            ],
            "/dev": [
                {
                    "path": "/embed",
                    "method": "POST",
                    "description": "Creates vector embeddings representing the input text. Includes all routes that have /user"
                }
            ],
            "/op": [
                {
                    "path": "/models/create",
                    "method": "POST",
                    "description": "Creates a new model from a configuration or modelfile. Includes all routes from /dev and /user"
                },
                {
                    "path": "/models/delete",
                    "method": "DELETE",
                    "description": "Deletes a model from the system"
                },
                {
                    "path": "/models/pull",
                    "method": "POST",
                    "description": "Pulls a model from a remote registry"
                },
                {
                    "path": "/models/push",
                    "method": "POST",
                    "description": "Pushes a local model to a remote registry"
                },
                {
                    "path": "/models/copy",
                    "method": "POST",
                    "description": "Creates a copy of an existing model"
                },
                {
                    "path": "/models/tags",
                    "method": "GET",
                    "description": "Lists all available model tags"
                },
                {
                    "path": "/system/ps",
                    "method": "GET",
                    "description": "Shows running inference processes and model usage"
                },
                {
                    "path": "/system/version",
                    "method": "GET",
                    "description": "Returns engine and API version information"
                }
            ]
        },
        "telemetry": {
            "uptime": f"{round(time.time() - START_TIME, 2)}s",
            "cpu_load": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "status": "Healthy"
        },
        "links": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "repository": "github.com/your-repo/infra"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("LOCAL_API_IP"), port=int(os.getenv("LOCAL_API_PORT")))
