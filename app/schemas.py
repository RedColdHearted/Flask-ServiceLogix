from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum

class RepairRequestStatus(Enum):
    NEW = "Новая заявка"
    IN_PROGRESS = "В процессе ремонта"
    COMPLETED = "Завершена"

class RepairRequestCreate(BaseModel):
    device_type: str
    device_model: str
    issue_description: str
    client_name: str
    client_phone: str

class RepairRequestUpdateStatus(BaseModel):
    status: RepairRequestStatus

class RepairRequestResponse(BaseModel):
    id: UUID
    request_date: datetime
    device_type: str
    device_model: str
    issue_description: str
    client_name: str
    client_phone: str
    status: RepairRequestStatus

    class Config:
        orm_mode = True