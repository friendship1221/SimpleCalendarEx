from pydantic import BaseModel
from datetime import date
from typing import Optional
import uuid

class DayOffDto(BaseModel):
    id: Optional[uuid.UUID] = None
    organid: Optional[str] = None
    dayoff: date
    year: Optional[int] = None
    description: Optional[str] = None
    creator: Optional[str] = None
    createdate: Optional[date] = None
    modifier: Optional[str] = None
    modifydate: Optional[date] = None
    delflag: Optional[int] = 0
    
    class Config:
        from_attributes = True

class DayOffCreateRequest(BaseModel):
    dayoff: str  # format dd/MM/yyyy
    isOffDay: bool
    description: Optional[str] = None
    creator: str
    organid: Optional[str] = None

class DayOffDeleteRequest(BaseModel):
    dayoff: str  # format dd/MM/yyyy
    organid: str

class DayOffSearchRequest(BaseModel):
    dayoffFrom: str  # format dd/MM/yyyy
    dayoffTo: str    # format dd/MM/yyyy
    organid: str

class DayOffCheckRequest(BaseModel):
    dayoff: str  # format dd/MM/yyyy
    organid: str

class DayOffCheckResponse(BaseModel):
    is_off_day: bool