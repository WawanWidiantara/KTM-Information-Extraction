from fastapi import HTTPException
from app.schemas.profile import Profile
import locale

import pytesseract

import re
from datetime import datetime
from PIL import Image

def preprocess_image(image):
    # rezise the image width=984 and height=699
    image = image.resize((984, 699))

    print(image.size)

    personal_info_config = {
        "left": 240,
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

def clean_text(text):
    # Cleaning the text
    text = re.split(r'Kartu Mahasiswa Elektronik', text)[0]
    text = re.sub(r'.*Nama\s*:', 'Nama :', text, flags=re.DOTALL)
    text = re.sub(r'[_—\-]+|Berlaku s/d', ' ', text).strip()
    return text

def preprocess_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if len(line) > 0]
    lines = [re.sub(r'\W', ' ', line) for line in lines]
    lines = [line.strip() for line in lines]
    lines = [re.sub(r' +', ' ', line) for line in lines]
    lines = [line.upper() for line in lines]
    return lines

def preprocess_text(text):
    text = clean_text(text)
    # Regular expressions to capture the required data
    name_re = r"Nama\s*:\s*\|?(.*)"
    npm_re = r"NPM\s*:\s*(\d+)"
    faculty_re = r"Fakultas\s*:\s*(.*)"
    study_program_re = r"Program Studi\s*:\s*(.*)"
    program_re = r"Program\s*:\s*(.*)"
    date_re = r"\d{1,2}\s+\w+\s+\d{4}" 
    address_re = r"Alamat\s*:\s*(.*)"

    # Extracting the data
    name = re.search(name_re, text).group(1).strip()
    npm = re.search(npm_re, text).group(1).strip()
    faculty = re.search(faculty_re, text).group(1).strip()
    study_program = re.search(study_program_re, text).group(1).strip()
    program = re.search(program_re, text).group(1).strip()

    # Extract both dates and address
    dates = re.findall(date_re, text)
    dob = dates[0].strip()
    expiry_date = dates[1].strip()
    text = re.sub(expiry_date, '', text).strip()

    address = re.search(address_re, text, re.DOTALL).group(1).strip()
    address = re.sub(r'\s+', ' ', address)

    # Helper function for parsing dates
    def parse_date(date_str):
        for loc in ['en_US.UTF-8', 'id_ID.UTF-8']:
            try:
                locale.setlocale(locale.LC_TIME, loc)
                return datetime.strptime(date_str, "%d %B %Y").date()
            except ValueError:
                continue
        raise ValueError("Date format not recognized")
    
    # Converting dates
    dob_converted = parse_date(dob)
    expiry_date_converted = parse_date(expiry_date)

    # Constructing the result dictionary
    result = {
        "name": name,
        "npm": npm,
        "faculty": faculty,
        "study_program": study_program,
        "program": program,
        "dob": dob_converted.isoformat(),
        "address": address,
        "ktm_image_url": "",
        "expired_at": expiry_date_converted.isoformat(),
        "created_at": datetime.now().isoformat()
    }
    return result

async def ocr_extract(image: Image, image_url: str):
    config = '--psm 4 --oem 3'

    try:
        text = pytesseract.image_to_string(image, config=config)
        ocr_extract = preprocess_text(text)
        ocr_extract["ktm_image_url"] = image_url
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid KTM file")
    
    return Profile(**ocr_extract)