from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
import uuid

from app.db.database import get_db
from app.models.dayoff import DayOffYear
from app.models.schemas import (
    DayOffDto, 
    DayOffCreateRequest, 
    DayOffDeleteRequest, 
    DayOffSearchRequest, 
    DayOffCheckRequest,
    DayOffCheckResponse
)

router = APIRouter(prefix="/api/dayoff", tags=["dayoff"])

def parse_date(date_str: str) -> date:
    """Parse date string in dd/MM/yyyy format"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Expected dd/MM/yyyy")

@router.post("/create", response_model=DayOffDto)
async def create_or_edit_dayoff(request: DayOffCreateRequest, db: Session = Depends(get_db)):
    """
    Create or edit a day off record
    """
    dayoff_date = parse_date(request.dayoff)
    
    # Check if record already exists
    existing_record = db.query(DayOffYear).filter(
        DayOffYear.dayoff == dayoff_date,
        DayOffYear.organid == request.organid,
        DayOffYear.delflag == 0
    ).first()
    
    if existing_record:
        # Update existing record
        existing_record.description = request.description
        existing_record.modifier = request.creator
        existing_record.modifydate = date.today()
        if not request.isOffDay:
            existing_record.delflag = 1  # Mark as deleted if not an off day
        
        db.commit()
        db.refresh(existing_record)
        return DayOffDto.from_orm(existing_record)
    else:
        # Create new record only if it's an off day
        if request.isOffDay:
            new_record = DayOffYear(
                id=uuid.uuid4(),
                organid=request.organid,
                dayoff=dayoff_date,
                year=dayoff_date.year,
                description=request.description,
                creator=request.creator,
                createdate=date.today(),
                delflag=0
            )
            
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return DayOffDto.from_orm(new_record)
        else:
            raise HTTPException(status_code=400, detail="Cannot create a non-off day record")

@router.delete("/delete", response_model=DayOffDto)
async def delete_dayoff(request: DayOffDeleteRequest, db: Session = Depends(get_db)):
    """
    Delete a day off record (soft delete)
    """
    dayoff_date = parse_date(request.dayoff)
    
    record = db.query(DayOffYear).filter(
        DayOffYear.dayoff == dayoff_date,
        DayOffYear.organid == request.organid,
        DayOffYear.delflag == 0
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Day off record not found")
    
    record.delflag = 1
    record.modifydate = date.today()
    
    db.commit()
    db.refresh(record)
    
    return DayOffDto.from_orm(record)

@router.post("/search", response_model=List[DayOffDto])
async def search_dayoffs(request: DayOffSearchRequest, db: Session = Depends(get_db)):
    """
    Search for day off records within a date range
    """
    from_date = parse_date(request.dayoffFrom)
    to_date = parse_date(request.dayoffTo)
    
    if from_date > to_date:
        raise HTTPException(status_code=400, detail="From date cannot be later than to date")
    
    records = db.query(DayOffYear).filter(
        DayOffYear.dayoff >= from_date,
        DayOffYear.dayoff <= to_date,
        DayOffYear.organid == request.organid,
        DayOffYear.delflag == 0
    ).order_by(DayOffYear.dayoff).all()
    
    return [DayOffDto.from_orm(record) for record in records]

@router.post("/check", response_model=DayOffCheckResponse)
async def check_dayoff(request: DayOffCheckRequest, db: Session = Depends(get_db)):
    """
    Check if a specific date is an off day
    """
    dayoff_date = parse_date(request.dayoff)
    
    record = db.query(DayOffYear).filter(
        DayOffYear.dayoff == dayoff_date,
        DayOffYear.organid == request.organid,
        DayOffYear.delflag == 0
    ).first()
    
    return DayOffCheckResponse(is_off_day=record is not None)