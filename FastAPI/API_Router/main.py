from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .convert import router as convert_router
from .generate_info import router as generate_info_router
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="Audio Processing Pipeline",
    version="1.0.0"
)


origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Or specify ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)

app.include_router(convert_router)
app.include_router(generate_info_router)
