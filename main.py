from json import load
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os
load_dotenv()
ENV = os.getenv('ENV')


main_app = FastAPI(
    title = "Shilajit Tea API",
    description= "Backend for ShilajitTea API",
    version = "1.0.0"
)

@main_app.get('/')
async def root():
    return {"message" : "Welcome to Shilajit API"}

@main_app.get('/health')
async def health_check():
    return {"status":"healthy"}


if __name__ == "__main__":
    if ENV == 'LOCAL':
        uvicorn.run(main_app,reload=True,host='0.0.0.0',port = 8000)
    else:
        print('produciton bob')
