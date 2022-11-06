from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import url, user
from datetime import datetime

app = FastAPI(title='URL Shortner', root_path='/')
app.include_router(user.router)
app.include_router(url.router)

origins = [
    "http://localhost",
    "http://localhost:3000"
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="origins",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization","*"],
    expose_headers=["Date", "x-api-id"],
    max_age=300
)

@app.get('/')
async def root():
    return {'msg': f"I'm alive {datetime.now()}"}