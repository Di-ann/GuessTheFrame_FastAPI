from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()

router = APIRouter()

@router.get("/")
async def get():
    if __name__ == 'main':
        uvicorn.run()