from sqlalchemy import Column, String, Date, Integer, Text, UUID
from app.db.database import Base
import uuid

class DayOffYear(Base):
    __tablename__ = "daysoffyear"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organid = Column(String(250))
    dayoff = Column(Date)
    year = Column(Integer)
    description = Column(Text)
    creator = Column(String(250))
    createdate = Column(Date)
    modifier = Column(String(250))
    modifydate = Column(Date)
    delflag = Column(Integer, default=0)  # 0 = not deleted, 1 = deleted