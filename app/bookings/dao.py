from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        with booked_rooms as (
            select * from bookings
            where room_id = 1 and
            (date_from >= '2023-05-15' and date_from <= '2023-06-20') or
            (date_from <= '2023-05-15' and date_to > '2023-05-15')
        )
        select rooms.quantity - count(booked_rooms.room_id) from rooms
        left join booked_rooms on booked_rooms.room_id = rooms.id
        where rooms.id = 1
        group by rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity)
                )
                # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left is not None and rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database"
            elif isinstance(e, Exception):
                msg = "Unknown"
            msg += " Exception: Cannot add booking"
            extra = {"user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)


    @classmethod
    async def delete_booking(cls, booking_id, current_user):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    bookings = select(Bookings).where(
                        and_(
                            Bookings.id == booking_id,
                            Bookings.user_id == current_user.id,
                        )
                    )
                    await session.execute(
                        delete(Bookings).where(Bookings.id == booking_id)
                    )
                    await session.commit()
                    return {"status": "Успех", "message": "Booking удален"}
                except Exception as e:
                    await session.rollback()
                    return e
