from .database import Database
from ..models import User

def get_by_user_id(user_id: int) -> User :
    db = Database()
    db.execute(f"select * from users where user_id = '{user_id}'")
    rows = db.fetchall()
    db.close()
    users = [User(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return users[0] if users else None

def get_by_email(email: str) -> User :
    db = Database()
    db.execute(f"select * from users where email = '{email}'")
    rows = db.fetchall()
    db.close()
    users = [User(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return users[0] if users else None