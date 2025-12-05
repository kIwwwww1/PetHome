import uvicorn
from fastapi import FastAPI
# 
from .api.crud import user_router
 
app = FastAPI()

app.include_router(user_router)

@app.get('/')
async def start_endpoint():
    return {'True': 'Твое сообщение'}


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8000, reload=True)