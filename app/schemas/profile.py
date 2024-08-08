from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Literal, Optional

class Profile(BaseModel):
    name: str
    npm: str
    faculty: str
    study_program: str
    program: str
    dob: date
    address: str
    ktm_image_url: Optional[str] = None
    expired_at: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)
