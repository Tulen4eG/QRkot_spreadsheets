from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import CharityDonationBase


class Donation(CharityDonationBase):
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False,
        name='fk_donation_user_id_user'
    )
    comment = Column(Text, nullable=True)

    user = relationship('User')

    def __repr__(self):
        return f'{super().__repr__()}, {self.user.email=}'
