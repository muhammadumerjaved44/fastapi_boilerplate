from fastapi import FastAPI
from routes import utils
from config import settings
from db.session import engine, Base

# declaring FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

# create all tables for first time
Base.metadata.create_all(bind=engine)

# routes
app.include_router(utils.router, prefix="/utils", tags=["utils"])
