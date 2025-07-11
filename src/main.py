from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter
import uvicorn
from src.quiz.router import router as quiz_router
from src.admin.router import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(admin_router)
app.include_router(quiz_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

