import uvicorn
from fastapi import FastAPI
from routes import utils, auth, users
from config import settings
from uvicorn.config import LOGGING_CONFIG
from db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from db.initialize_db import initialize_db

# declaring FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

# create all tables for first time
Base.metadata.create_all(bind=engine)

# inserting initial database data
initialize_db()

# routes
app.include_router(utils.router, prefix="/utils", tags=["utils"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":

    # adding datetime in the uvicorn logs of endpoints
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(levelprefix)s %(asctime)s, %(message)s"

    uvicorn.run(
        "main:app", host="0.0.0.0", port=settings.API_PORT_DOCKER, reload=settings.DEBUG
    )
