import uvicorn
from fastapi import FastAPI
 
app = FastAPI()

@app.get('/')
async def start_endpoint():
    return {'True': 'Твое сообщение'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)