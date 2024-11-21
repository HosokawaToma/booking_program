from .database import Database
from ..models import UserLiff

def get_by_user_liff_id(user_liff_id: str)-> UserLiff :
    db = Database()
    db.execute(f"select * from users_liff where user_liff_id = '{user_liff_id}'")
    rows = db.fetchall()
    db.close()
    users_liff = [UserLiff(row[0], row[1]) for row in rows]
    return users_liff[0] if users_liff else None

def get_by_user_id(user_id: str)-> list[UserLiff] :
    db = Database()
    db.execute(f"select * from users_liff where user_id = '{user_id}'")
    rows = db.fetchall()
    db.close()
    users_liff = [UserLiff(row[0], row[1]) for row in rows]
    return users_liff

def insert(user_liff: UserLiff):
    db = Database()
    db.execute(f"INSERT INTO `users_liff` (`user_id`, `user_liff_id`) VALUES ('{user_liff.user_id}', '{user_liff.user_liff_id}')")
    db.commit()
    db.close()