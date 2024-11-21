import datetime
import os

def LINE_CLIENT_ID():
    return os.environ['LINE_CLIENT_ID']

def DATABASE_SOCKET():
    return os.environ['DATABASE_SOCKET']

def DATABASE_USER():
    return os.environ['DATABASE_USER']

def DATABASE_PASSWORD():
    return os.environ['DATABASE_PASSWORD']

def DATABASE_NAME():
    return os.environ['DATABASE_NAME']

def database_charset():
    return "utf8"

def now_year():
    return datetime.datetime.now().year

def now_month():
    return datetime.datetime.now().month

def now_day():
    return datetime.datetime.now().day

def days_in_month():
    return 31

def period_in_day():
    return 6

def booking_title_list():
    return ['Valorant', 'Fortnite']

def individualized_teaching_course_type():
    return 2