from .database import Database
from ..config import now_year, now_month
from ..models import Capacity

def get_by_title_year_month(title: str, year_later: int = 0, month_later: int = 0) -> list[Capacity] :
    db = Database()
    db.execute(f"select * from capacities where title = '{title}' and {year_later + now_year()} = year and {month_later + now_month()} = month order by year, month, day, period")
    rows = db.fetchall()
    db.close()
    capacities = [Capacity(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    return capacities