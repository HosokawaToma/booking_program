import os
from flask import Flask, render_template, request
from lib import api
from lib import database
from lib import config
from lib import utilities

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template('booking_confirmation/index.html')

@app.route("/select", methods=['GET', 'POST'])
def booking_confirmation():
    if not request.method == "POST":
        return render_template('error.html', errorId='BB-001', errorStr='通信エラーです。適切な手順でページを開いてください。')

    liff_id_token = request.form["liff_id_token"]

    try:
        line_user_info = api.line_login.validate_id_token(liff_id_token)
        user_liff = database.users_liff.get_by_user_liff_id(line_user_info.sub)
        user = database.users.get_by_user_id(user_liff.user_id)
        today_bookings = database.bookings.get_by_user_id_year_month_day(user.user_id)
        now_month_after_day_bookings = database.bookings.get_by_user_id_year_month_after_day(user.user_id)
        next_month_bookings = database.bookings.get_by_user_id_year_month(user.user_id, month_later=1)
        absences = []
        for booking in today_bookings:
            absence = database.absences.get_by_booking(booking)
            absences.append(absence)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return render_template('error.html', errorId='BC-001', errorStr='内部エラーです。適切な手順でページを開いてください。')
    
    # コースタイプが個人授業ではない場合は接続できない
    if not user.course_type == config.individualized_teaching_course_type():
        return render_template('error.html', errorId='BB-003', errorStr='接続エラーです。あなたはこのURLに接続できません。')
    
    today_bookings_int_list = utilities.bookings_object_list_to_int_list(today_bookings)
    now_month_after_day_bookings_remove_absence = utilities.bookings_remove_absences(now_month_after_day_bookings, absences)
    bookings_int_list = utilities.bookings_object_list_to_int_list(now_month_after_day_bookings_remove_absence + next_month_bookings)

    return render_template('booking_confirmation/select.html', user_id=user.user_id, bookings=bookings_int_list, today_bookings=today_bookings_int_list)

@app.route("/check", methods=['GET', 'POST'])
def booking_confirmation_check():
    if not request.method == "POST":
        return render_template('error.html', errorId='BB-001', errorStr='通信エラーです。適切な手順でページを開いてください。')

    user_id = request.form["user_id"]
    booking = request.form.get("booking")
    today_booking = request.form.get("today_booking")

    try:
        user_liff = database.users_liff.get_by_user_id(user_id)

        if booking:
            cancel_booking = utilities.booking_str_to_object(booking)
            database.bookings.delete(cancel_booking)
            booking_number = utilities.bookings_object_list_to_int_list([cancel_booking])[0]
            # LINEとDiscordにメッセージを送信
            return render_template('booking_confirmation/check.html', booking=booking_number, info_text='上記の予約を取り消しました。')

        if today_booking:
            absence_booking = utilities.booking_str_to_object(today_booking)
            absence = utilities.booking_to_absence(absence_booking)
            database.absences.insert(absence)
            booking_number = utilities.bookings_object_list_to_int_list([absence])[0]
            # LINEとDiscordにメッセージを送信
            return render_template('booking_confirmation/check.html', booking=booking_number, info_text='上記の予約に欠席連絡をしました。')

    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return render_template('error.html', errorId='BC-001', errorStr='内部エラーです。適切な手順でページを開いてください。')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))