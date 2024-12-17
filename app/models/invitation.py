from sqlalchemy import Column, String, Boolean
from database import Base

class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(String, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    accepted = Column(Boolean, default=False)
