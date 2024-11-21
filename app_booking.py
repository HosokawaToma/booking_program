import os
from flask import Flask, render_template, request
from lib import api
from lib import database
from lib import config
from lib import utilities

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def booking():
    return render_template('booking/index.html')


@app.route("/select", methods=['GET', 'POST'])
def booking_select():
    if not request.method == "POST":
        return render_template('error.html', errorId='BB-001', errorStr='通信エラーです。適切な手順でページを開いてください。')

    title = request.form["title"]
    liff_id_token = request.form["liff_id_token"]

    try:
        line_user_info = api.line_login.validate_id_token(liff_id_token)
        user_liff = database.users_liff.get_by_user_liff_id(line_user_info.sub)
        user = database.users.get_by_user_id(user_liff.user_id)
        now_month_user_bookings = database.bookings.get_by_user_id_year_month(user.user_id)
        next_month_user_bookings = database.bookings.get_by_user_id_year_month(user.user_id, month_later=1)
        now_month_bookings = database.bookings.get_by_title_year_month(title)
        next_month_bookings = database.bookings.get_by_title_year_month(title, month_later=1)
        now_month_capacities = database.capacities.get_by_title_year_month(title)
        next_month_capacities = database.capacities.get_by_title_year_month(title, month_later=1)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return render_template('error.html', errorId='BB-002', errorStr='内部エラーです。適切な手順でページを開いてください。')

    print("now_month_user_bookings: ", now_month_user_bookings)

    # コースタイプが個人授業ではない場合は接続できない
    if not user.course_type == config.individualized_teaching_course_type():
        return render_template('error.html', errorId='BB-003', errorStr='接続エラーです。あなたはこのURLに接続できません。')

    # ユーザの予約上限数と塾の予約容量の計算
    now_month_booking_capacity = user.booking_capacity - len(now_month_user_bookings)
    next_month_booking_capacity = user.booking_capacity - len(next_month_user_bookings)

    now_month_capacities_number_list = utilities.capacities_verification_and_to_number_list(now_month_bookings, now_month_capacities, now_month_user_bookings)
    next_month_capacities_number_list = utilities.capacities_verification_and_to_number_list(next_month_bookings, next_month_capacities, next_month_user_bookings)

    return render_template(
        'booking/select.html',
        title=title,
        user_id=user.user_id,
        now_month_booking_capacity=now_month_booking_capacity,
        next_month_booking_capacity=next_month_booking_capacity,
        now_month_capacities_data=now_month_capacities_number_list[config.now_day()+1:],
        next_month_capacities_data=next_month_capacities_number_list
    )


@app.route("/check", methods=['GET', 'POST'])
def booking_check():
    if not request.method == "POST":
        return render_template('error.html', errorId='BC-001', errorStr='通信エラーです。適切な手順でページを開いてください。')

    title = request.form.get('title')
    user_id = request.form.get('user_id')
    now_month_bookings_str_list = request.form.getlist('now_month_select_bookings')
    next_month_bookings_str_list = request.form.getlist('next_month_select_bookings')

    try:
        user = database.users.get_by_user_id(user_id)
        users_liff = database.users_liff.get_by_user_id(user_id)
        now_month_user_bookings = database.bookings.get_by_user_id_year_month(user_id)
        next_month_user_bookings = database.bookings.get_by_user_id_year_month(user_id, month_later=1)
        now_month_bookings = database.bookings.get_by_title_year_month(title)
        next_month_bookings = database.bookings.get_by_title_year_month(title, month_later=1)
        now_month_capacities = database.capacities.get_by_title_year_month(title)
        next_month_capacities = database.capacities.get_by_title_year_month(title, month_later=1)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return render_template('error.html', errorId='BC-002', errorStr='内部エラーです。適切な手順でページを開いてください。')

    # コースタイプが個人授業ではない場合は接続できない
    if not user.course_type == config.individualized_teaching_course_type():
        return render_template('error.html', errorId='BB-003', errorStr='接続エラーです。あなたはこのURLに接続できません。')

    # ユーザの予約上限数と塾の予約容量の計算
    now_month_booking_capacity = user.booking_capacity - len(now_month_user_bookings)
    next_month_booking_capacity = user.booking_capacity - len(next_month_user_bookings)
    now_month_capacities_number_list = utilities.capacities_verification_and_to_number_list(now_month_bookings, now_month_capacities, now_month_user_bookings)
    next_month_capacities_number_list = utilities.capacities_verification_and_to_number_list(next_month_bookings, next_month_capacities, next_month_user_bookings)

    # select_bookings（strのlist）をbookings_schedule（Bookingオブジェクトのlist）に変換
    now_month_bookings_schedule = utilities.bookings_str_list_to_object_list(now_month_bookings_str_list, user_id)
    next_month_bookings_schedule = utilities.bookings_str_list_to_object_list(next_month_bookings_str_list, user_id)

    # 予約可能かどうかの確認
    if not (utilities.bookings_verification(now_month_bookings_schedule, now_month_capacities_number_list) or
            utilities.bookings_verification(next_month_bookings_schedule, next_month_capacities_number_list)):
        return render_template('error.html', errorId='BC-004', errorStr='内部エラーです。適切な手順でページを開いてください。')

    # 予約可能数以上の予約を行おうとしている場合
    if not (now_month_booking_capacity - len(now_month_bookings_schedule) < 0 or next_month_booking_capacity - len(next_month_bookings_schedule)):
        return render_template('error.html', errorId='BC-004', errorStr='内部エラーです。適切な手順でページを開いてください。')

    # LINEとDiscordにメッセージを送信

    # 予約操作
    try:
        for booking in now_month_bookings_schedule:
            database.bookings.insert(booking)
        for booking in next_month_bookings_schedule:
            database.bookings.insert(booking)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return render_template('error.html', errorId='BC-008', errorStr='内部エラーです。適切な手順でページを開いてください。')

    bookings = utilities.bookings_object_list_to_int_list(now_month_bookings_schedule + next_month_bookings_schedule)
    return render_template('booking/check.html', title=title, user_id=user_id, bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))