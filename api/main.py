from fastapi import FastAPI
from routes import utils
from config import settings


# declaring FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

# routes
app.include_router(utils.router, prefix="/utils", tags=["utils"])
