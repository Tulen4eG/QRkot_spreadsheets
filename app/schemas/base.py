from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, PositiveInt


class CharityDonationBase(BaseModel):
    full_amount: PositiveInt


class CharityDonationDBBase(CharityDonationBase):
    invested_amount: int
    fully_invested: bool
    create_date: dt
    close_date: Optional[dt]

    class Config:
        orm_mode = True
