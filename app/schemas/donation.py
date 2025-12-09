from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field

from app.core.constants import MIN_STR_LENGTH
from app.schemas.base import CharityDonationBase, CharityDonationDBBase


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, min_length=MIN_STR_LENGTH)


class DonationCreate(CharityDonationBase, DonationBase):
    pass


class DonationDBShort(DonationBase, CharityDonationBase):
    id: int
    create_date: dt

    class Config:
        orm_mode = True


class DonationDB(DonationDBShort, CharityDonationDBBase):
    user_id: int

    class Config:
        orm_mode = True
