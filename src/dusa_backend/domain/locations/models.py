from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Location(BaseModel):
    created: datetime
    longitude: Decimal
    latitude: Decimal
