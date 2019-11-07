from fastapi import APIRouter, FastAPI, HTTPException
from starlette.responses import JSONResponse
import os
from .routers import trades
from starlette.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware
# import uuid
from fastapi.exceptions import RequestValidationError, ValidationError
# from starlette.middleware.gzip import GZipMiddleware


app = FastAPI(title="Backend Test API", description="Service for receiving trades from the outside world", version="1.0.0",
              docs_url="/docs", default_response_class=JSONResponse)
app.add_middleware(CORSMiddleware, allow_origins=['*'])
#app.add_middleware(SessionMiddleware, secret_key=uuid.uuid1())
app.include_router(trades.router, prefix="/v1/trades", tags=["Trades"])

app.debug = True
env: dict = os.environ
if env.setdefault('PYTHON_ENV', '').title() == 'Development':
    app.debug = True


@app.exception_handler(HTTPException)
async def http_exception(request, exc):
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


# @app.exception_handler(RequestValidationError)
# async def request_validation_exception_handler(request, exc):
#     return JSONResponse({"message": exc.detail}, status_code=exc.status_code)
#     # app.add_middleware(http_exception())


# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


@app.on_event('startup')
async def server_startup():
    print("App server is running at port 8080")
