from .database import Database
from ..config import now_year, now_month, now_day
from ..models import Booking

def get_by_title_year_month(title: str, year_later: int = 0, month_later: int = 0) -> list[Booking] :
    db = Database()
    db.execute(f"select * from bookings where title = '{title}' and {now_year() + year_later} = year and {now_month() + month_later} = month order by year, month, day, period")
    rows = db.fetchall()
    db.close()
    bookings = [Booking(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return bookings

def get_by_user_id_year_month(user_id: int, year_later: int = 0, month_later: int = 0) -> list[Booking] :
    db = Database()
    db.execute(f"select * from bookings where user_id = {user_id} and {now_year() + year_later} = year and {now_month() + month_later} = month order by year, month, day, period")
    rows = db.fetchall()
    db.close()
    bookings = [Booking(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return bookings

def get_by_user_id_year_month_day(user_id: int, year_later: int = 0, month_later: int = 0, day_later: int = 0) -> list[Booking] :
    db = Database()
    db.execute(f"select * from bookings where user_id = {user_id} and {now_year() + year_later} = year and {now_month() + month_later} = month and day = {now_day() + day_later} order by year, month, day, period")
    rows = db.fetchall()
    db.close()
    bookings = [Booking(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return bookings

def get_by_user_id_year_month_after_day(user_id: int, year_later: int = 0, month_later: int = 0, after_day: int = now_day()) -> list[Booking] :
    db = Database()
    db.execute(f"select * from bookings where user_id = {user_id} and {now_year() + year_later} = year and {now_month() + month_later} = month and day > {after_day} order by year, month, day, period")
    rows = db.fetchall()
    db.close()
    bookings = [Booking(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return bookings

def insert(booking: Booking):
    db = Database()
    db.execute(f"insert into bookings (year, month, day, period, title, user_id) values ('{booking.year}', '{booking.month}', '{booking.day}', '{booking.period}', '{booking.title}', '{booking.user_id}')")
    db.commit()
    db.close()

def delete(booking: Booking):
    db = Database()
    db.execute(f"DELETE FROM bookings WHERE user_id = {booking.user_id} and {booking.year} = year and {booking.month} = month and day = {booking.day} and period = {booking.period} and title = '{booking.title}' and user_id = {booking.user_id}")
    db.commit()
    db.close()