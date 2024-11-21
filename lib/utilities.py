from .models import Booking, Capacity, Absence, LineUserInfo
from .config import days_in_month, period_in_day

def capacities_verification_and_to_number_list(bookings: list[Booking], capacities: list[Capacity], user_bookings: list[Booking]) -> list[int]:
    year_index = 0
    month_index = 1
    day_index = 2
    period_index = 3
    capacity_index = 4
    capacities_number_list = [[[0, 0, 0, 0, 0] for _ in range(period_in_day())] for _ in range(days_in_month())]

    for i in range(days_in_month()):
        for j in range(period_in_day()):
            capacities_number_list[i][j][day_index] = i + 1
            capacities_number_list[i][j][period_index] = j + 1

    for capacity in capacities:
        capacities_number_list[capacity.day - 1][capacity.period - 1][year_index] = capacity.year
        capacities_number_list[capacity.day - 1][capacity.period - 1][month_index] = capacity.month
        capacities_number_list[capacity.day - 1][capacity.period - 1][day_index] = capacity.day
        capacities_number_list[capacity.day - 1][capacity.period - 1][period_index] = capacity.period
        capacities_number_list[capacity.day - 1][capacity.period - 1][capacity_index] = capacity.capacity

    for booking in bookings:       
        capacities_number_list[booking.day - 1][booking.period - 1][capacity_index] -= 1
        if  capacities_number_list[booking.day - 1][booking.period - 1][capacity_index] < 0:
            return []
    
    for booking in user_bookings:
        print("utilities: ", booking.day - 1, booking.period - 1)
        capacities_number_list[booking.day - 1][booking.period - 1][capacity_index] = -1
    
    return capacities_number_list

def bookings_str_list_to_object_list(bookings_str_list: list[str], user_id) -> list[Booking]:
    return_bookings = []
    for booking_str in bookings_str_list:
        booking = booking_str.split('-')
        return_bookings.append(Booking(int(booking[0]), int(booking[1]), int(booking[2]), int(booking[3]), booking[4], int(user_id)))
    return return_bookings

def bookings_verification(bookings_schedule: list[Booking], capacities_number_list: list[int]) -> bool:
    period_index = 3
    for booking in bookings_schedule:
        if capacities_number_list[booking.day][booking.period][period_index] < 1:
            return False
    return True

def bookings_object_list_to_int_list(bookings_object_list: list[Booking]) -> list[int]:
    return [[x.year, x.month, x.day, x.period, x.title, x.user_id] for x in bookings_object_list]

def booking_str_to_object(booking_str: str) -> Booking:
    b = booking_str.split('-')
    return Booking(b[0], b[1], b[2], b[3], b[4], b[5])

def booking_to_absence(booking: Booking) -> Absence:
    return Absence(booking.year, booking.month, booking.day, booking.period, booking.title, booking.user_id)

def bookings_remove_absences(bookings: list[Booking], absences: list[Absence]) -> list[Booking]:
    return_bookings = [booking for booking in bookings]
    for booking in bookings:
        for absence in absences:
            if booking.to_dict() == absence.to_dict():
                return_bookings.remove(booking)
    return return_bookings

def parse_line_user_info(json_data: dict) -> LineUserInfo:
    return LineUserInfo(
        iss=json_data.get("iss"),
        sub=json_data.get("sub"),
        aud=json_data.get("aud"),
        exp=json_data.get("exp"),
        iat=json_data.get("iat"),
        nonce=json_data.get("nonce"),
        amr=json_data.get("amr"),
        name=json_data.get("name"),
        picture=json_data.get("picture"),
        email=json_data.get("email"),
    )