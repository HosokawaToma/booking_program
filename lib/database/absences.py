from .database import Database
from ..config import now_year, now_month, now_day
from ..models import Absence, Booking

def get_by_booking(booking: Booking) -> Absence:
    db = Database()
    db.execute(f"select * from booking where user_id = {booking.user_id} and {booking.year} = year and {booking.month} = month and {booking.day} = day and {booking.period} = period and {booking.title} = title order by year, month, day, period")
    rows = db.fetchall()
    db.close()
    absences = [Absence(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return absences[0]

def insert(absence: Absence):
    db = Database()
    db.execute(f"insert into absences (year, month, day, period, title, user_id) values ('{absence.year}', '{absence.month}', '{absence.day}', '{absence.period}', '{absence.title}'), '{absence.user_id}'")
    db.commit()
    db.close()