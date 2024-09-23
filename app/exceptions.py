from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ''
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"

class No_existing_bookings_Exception(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="Такого букинга не существует"
class IncorrectEmailOrPassword(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Ваш токен истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"

class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Дата заселения в отель не может быть больше чем дата выселения"

class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Вы не можете заьронировать отель на такой длинный период"

class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Ошибка при добавлении данных в БД"

class CannotProcessCSV(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Ошибка при форматировании CSV файла"





