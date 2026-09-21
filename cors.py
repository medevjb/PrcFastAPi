from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

origin = os.getenv("ORIGIN").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)