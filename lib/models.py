from typing import List, Optional

class Booking():
    def __init__(self, year: int, month: int, day: int, period: int, title: str, user_id: int):
        self.year = year
        self.month = month
        self.day = day
        self.period = period
        self.title = title
        self.user_id = user_id

    def to_dict(self):
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "period": self.period,
            "title": self.title,
            "user_id": self.user_id
        }

class Absence():
    def __init__(self, year: int, month: int, day: int, period: int, title: str, user_id: int):
        self.year = year
        self.month = month
        self.day = day
        self.period = period
        self.title = title
        self.user_id = user_id

    def to_dict(self):
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "period": self.period,
            "title": self.title,
            "user_id": self.user_id
        }

class Capacity():
    def __init__(self, year: int, month: int, day: int, period: int, capacity: int, title: str):
        self.year = year
        self.month = month
        self.day = day
        self.period = period
        self.capacity = capacity
        self.title = title

    def to_dict(self):
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "period": self.period,
            "capacity": self.capacity
        }

class User():
    def __init__(self, user_id: int, name: str, course_type: int, booking_capacity: int, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.course_type = course_type
        self.booking_capacity = booking_capacity
        self.email = email
        self.password = password
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "course_type": self.course_type,
            "booking_capacity": self.booking_capacity,
            "email": self.email,
            "password": self.password
        }

class UserLiff():
    def __init__(self, user_id: int, user_liff_id: str):
        self.user_id = user_id
        self.user_liff_id = user_liff_id
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_liff_id": self.user_liff_id
        }

class LineUserInfo:
    def __init__(
        self,
        iss: str,
        sub: str,
        aud: str,
        exp: int,
        iat: int,
        nonce: Optional[str] = None,
        amr: Optional[List[str]] = None,
        name: Optional[str] = None,
        picture: Optional[str] = None,
        email: Optional[str] = None,
    ):
        self.iss = iss
        self.sub = sub
        self.aud = aud
        self.exp = exp
        self.iat = iat
        self.nonce = nonce
        self.amr = amr
        self.name = name
        self.picture = picture
        self.email = email

