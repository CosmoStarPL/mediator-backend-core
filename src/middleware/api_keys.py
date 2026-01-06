from fastapi import Request
from fastapi.responses import JSONResponse

API_KEYS = {
    "six_seven": {"client": "test", "role": "OP"},
    "forty_one": {"client": "test", "role": "DEV"},
    "nonchalant": {"client": "frontend", "role": "USER"},
    "anime_tyanka": {"client": "bot", "role": "OP"},
}

def api_check(authorization: str):
    if not authorization.startswith("Bearer "):
        return 401

    key = authorization.removeprefix("Bearer ")
    if "six_seven" not in API_KEYS.keys():
        return 403

    return API_KEYS[key]

async def auth_check(request: Request, call_next):
    auth = request.headers.get("Authorization")
    if request.url.path in ["/health", "/docs", "/api/v1/docs", "/openapi.json", "/api/v1/openapi.json"]:
        return await call_next(request)
    if not auth:
        return JSONResponse(
            status_code=401,
            content={"detail": "Not authorized. Go away."}
        )
    client = api_check(auth)
    if client == 401:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid credentials. Access denied."}
        )
    if client == 403:
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden. You are not welcome here."}
        )
    if client.get("role") == "USER":
        if request.url.path.startswith(("/dev", "/op")):
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden. You are not welcome here."}
            )
    if client.get("role") == "DEV":
        if request.url.path.startswith("/op"):
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden. You are not welcome here."}
            )
    return await call_next(request)