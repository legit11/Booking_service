from datetime import date, timedelta

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import (
    CannotBookHotelForLongPeriod,
    DateFromCannotBeAfterDateTo,
    RoomCannotBeBooked,
)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)

@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)): #-> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post('')
@version(1)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):

    if date_from >= date_to:
        raise DateFromCannotBeAfterDateTo
    elif date_to - date_from > timedelta(days=30):
        raise CannotBookHotelForLongPeriod

    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("")
@version(1)
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete_booking(booking_id, current_user)



