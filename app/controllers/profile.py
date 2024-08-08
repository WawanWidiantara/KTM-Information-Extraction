from fastapi import HTTPException
from app.schemas.profile import Profile
import locale

import pytesseract

import re
from datetime import datetime
from PIL import Image

def preprocess_image(image):
    personal_info_config = {
        "left": 260,
        "right": 850,
        "top": 200,
        "bottom": 625,
    }

    pp_expired_config = {
        "left": 0,
        "right": 275,
        "top": 200,
        "bottom": 650,
    }    

    personal_info = image.crop((personal_info_config["left"], personal_info_config["top"], personal_info_config["right"], personal_info_config["bottom"]))

    pp_expired = image.crop((pp_expired_config["left"], pp_expired_config["top"], pp_expired_config["right"], pp_expired_config["bottom"]))
    return personal_info, pp_expired

def preprocess_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if len(line) > 0]
    lines = [re.sub(r'\W', ' ', line) for line in lines]
    lines = [line.strip() for line in lines]
    lines = [re.sub(r' +', ' ', line) for line in lines]
    lines = [line.upper() for line in lines]
    return lines

async def ocr_extract(image: Image, image_url: str):
    config = '--psm 4 --oem 3'

    try:
        personal_info, pp_expired = preprocess_image(image)
        personal_info_text = pytesseract.image_to_string(personal_info, config=config)
        personal_info_lines = preprocess_text(personal_info_text)
        address_line = personal_info_lines[6:]
        address_line[0] = address_line[0].split('ALAMAT ')[1]
        address = ' '.join(address_line)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid KTM file")

    pp_expired_text = pytesseract.image_to_string(pp_expired, config=config)
    pp_expired_lines = preprocess_text(pp_expired_text)
    expired = pp_expired_lines[1]

    dob = personal_info_lines[5].split()
    dob = ' '.join(dob[-3:])

    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
    pp_expired = datetime.strptime(expired, '%d %B %Y').date()

    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    dob = datetime.strptime(dob, '%d %B %Y').date()

    data = {
        "name": personal_info_lines[0].split('NAMA ')[1],
        "npm": personal_info_lines[1].split('NPM ')[1],
        "faculty": personal_info_lines[2].split('FAKULTAS ')[1],
        "study_program": personal_info_lines[3].split('PROGRAM STUDI ')[1],
        "program": personal_info_lines[4].split('PROGRAM ')[1],
        "dob": dob,
        "address": address,
        "ktm_image_url": image_url,
        "expired_at": pp_expired,
    }

    return Profile(**data)