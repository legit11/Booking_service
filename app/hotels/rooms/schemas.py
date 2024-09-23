from typing import Optional

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    quantity: int
    image_id: int

    model_config = ConfigDict(orm_mode=True)


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    model_config = ConfigDict(orm_mode=True)
