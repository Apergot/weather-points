from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, Float
from sqlalchemy.dialects.postgresql import INTEGER, UUID
import uuid

Base = declarative_base()
metadata = Base.metadata


class Point(Base):
    __tablename__ = 'point'

    id = Column(INTEGER(), primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), unique=True)
    country = Column(String(255))
    region = Column(String(255))
    lat = Column(Float)
    lon = Column(Float)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, name, country, region, lat, lon):
        self.name = name
        self.country = country
        self.region = region
        self.lat = lat
        self.lon = lon

    def serialize(self):
        return {
            'uuid': self.uuid,
            'createdOn': self.created_on,
            'name': self.name,
            'country': self.country,
            'region': self.region,
            'lat': self.lat,
            'lon': self.lon
        }