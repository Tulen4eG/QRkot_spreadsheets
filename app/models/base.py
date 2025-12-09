from datetime import datetime as dt

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class CharityDonationBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='amount_must_be_positive'
        ),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='invested_amount_range_constraint'
        )
    )

    def __repr__(self):
        return (
            f'{type(self).__name__}'
            f'{self.id=}, '
            f'{self.full_amount=}, '
            f'{self.invested_amount=}, '
            f'{self.fully_invested=}, '
            f'{self.create_date=}, '
            f'{self.close_date=}'
        )
