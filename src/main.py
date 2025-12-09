import time
import logging
import uvicorn
from fastapi import FastAPI, Request
# 
from src.exception import logging_config
from .api.users_crud import user_router
from .api.pets_crud import dog_router
from .api.admin_crud import admin_router

logging_config(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(user_router)
app.include_router(dog_router)
app.include_router(admin_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} - status {response.status_code} - {process_time:.2f}ms"
    )
    return response
    

@app.get('/')
async def start_endpoint():
    return {'True': 'Твое сообщение'}


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8000, reload=True)