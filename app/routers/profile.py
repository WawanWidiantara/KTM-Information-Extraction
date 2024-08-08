from fastapi import APIRouter, HTTPException, status, File, UploadFile, Request
from app.schemas.profile import Profile
from app.controllers.profile import ocr_extract
from PIL import Image, UnidentifiedImageError
import io
import uuid
import os

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={404: {"description": "Not found"}},
)

@router.post("/extract")
async def extract_profile(
    request: Request,
    image: UploadFile = File(...),
):
    file_ext = image.filename.split(".")[-1]
    try:
        image = Image.open(io.BytesIO(image.file.read()))
    except UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    media_directory = os.path.join(os.path.dirname(__file__), '..', 'media')

    # Save the uploaded file
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_location = os.path.join(media_directory, filename)

    # Construct the image URL dynamically
    image_url = request.url_for("media", path=filename)
    profile = await ocr_extract(image, image_url._url)

    # Save the image
    image.save(file_location)

    return {"data": profile}