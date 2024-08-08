from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Literal, Optional

class Profile(BaseModel):
    name: str
    npm: int = Field(..., gt=0, lt=10**10)
    faculty: Literal["SAINS TEKNOLOGI", "BISNIS HUMANIORA"]
    study_program: str
    program: str
    dob: str
    address: str
    image: Optional[str] = None
    expired_at: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)
