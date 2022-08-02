import uvicorn
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=settings.API_PORT_DOCKER, reload=settings.DEBUG
    )
