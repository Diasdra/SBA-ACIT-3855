from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class Health(Base):
    """ Processing Statistics """

    __tablename__ = "health"

    id = Column(Integer, primary_key=True)
    storage = Column(String(250), nullable=False)
    receiver =Column(String(250), nullable=False)
    processor =Column(String(250), nullable=False)
    audit = Column(String(250), nullable=False)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, receiver, processor, audit, storage, 
        last_updated):

        """ Initializes a processing statistics object """
        self.storage = storage
        self.receiver = receiver
        self.processor = processor
        self.audit = audit
        self.last_updated = last_updated

    def to_dict(self):

        """ Dictionary Representation of a statistics """

        dict = {}
        dict['storage'] = self.storage
        dict['receiver'] = self.receiver
        dict['processor'] = self.processor
        dict['audit'] = self.audit
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")
        return dict