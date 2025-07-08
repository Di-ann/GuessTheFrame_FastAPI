from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter
import uvicorn

from src.admin.router import router as admin_router

app = FastAPI()

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/")
async def get():
    if __name__ == 'main':
        uvicorn.run()

app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(admin_router)