import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (4, "2030-05-04", "2030-05-25", 3, 200),
    (4, "2030-05-04", "2030-05-25", 4, 200),
    (4, "2030-05-04", "2030-05-25", 5, 200),
    (4, "2030-05-04", "2030-05-25", 6, 200),
    (4, "2030-05-04", "2030-05-25", 7, 200),
    (4, "2030-05-04", "2030-05-25", 8, 200),
    (4, "2030-05-04", "2030-05-25", 9, 200),
    (4, "2030-05-04", "2030-05-25", 10, 200),
    (4, "2030-05-04", "2030-05-25", 10, 409),
    (4, "2030-05-04", "2030-05-25", 10, 409),

])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code,
                                    booked_rooms,
                                   authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code

    responce = await authenticated_ac.get("/bookings")
    assert len(responce.json()) == booked_rooms

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2030-05-04", "2030-05-25", 200),
    (2, "2030-05-04", "2030-05-04", 409),
    (3, "2030-05-04", "2030-07-30", 409),
    (5, "2030-05-04", "2030-05-26", 200)
])
async def test_add_and_get_booking_with_date(room_id, date_from, date_to, status_code,
        authenticated_ac: AsyncClient):
        responce = await authenticated_ac.post("/bookings", params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        })
        assert responce.status_code == status_code


async def get_and_delete_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 200
    bookings = response.json()

    if not bookings:
        return  # Нет бронирований для удаления

    for booking in bookings:
        res = await authenticated_ac.delete(f"/bookings/{booking['id']}")
        assert res.status_code == 200
    result = await authenticated_ac.get("/bookings")
    assert len(result.json()) == 0


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2030-05-04", "2030-05-25", 200),
])
async def test_get_bookings(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    # Создание бронирования
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code, f"Ошибка создания бронирования: {response.json()}"

    booking_id = response.json().get('id')
    assert booking_id, f"Не удалось получить ID бронирования: {response.json()}"

    # Чтение созданного бронирования
    read_booking = await authenticated_ac.get(f"/bookings/{booking_id}")
    assert read_booking.status_code == 404, f"Ошибка получения бронирования: {read_booking.json()}"


