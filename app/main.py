from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.routers import profile
from app.config import settings
import pytesseract
import os

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Make sure media directory exists
media_directory = os.path.join(os.path.dirname(__file__), 'media')
os.makedirs(media_directory, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.1.0",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount the media directory to serve static files
app.mount("/media", StaticFiles(directory="app/media"), name="media")

# Include the routers
app.include_router(profile.router)