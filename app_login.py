import os
from flask import Flask, render_template, request
from lib import api
from lib import database
from lib import models

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template('login/index.html')

@app.route("/check", methods=["GET", "POST"])
def login_home():
    if not request.method == "POST":
        return render_template('error.html', errorId='LC-001', errorStr='通信エラーです。適切な手順でページを開いてください。')
    
    liff_id_token = request.form['liff_id_token']
    email = request.form['email']
    password = request.form['password']

    try:
        line_user_info = api.line_login.validate_id_token(liff_id_token)
        user = database.users.get_by_email(email)
        user_liff = database.users_liff.get_by_user_liff_id(line_user_info.sub)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return render_template('error.html', errorId='LC-002', errorStr='内部エラーです。適切な手順でページを開いてください。')

    if not user or user.password != password:
        return render_template('login/index.html', error_info='メールアドレスまたはパスワードが違います。')

    #user_idとwebhook_idの登録
    if not user_liff:
        try:
            database.users_liff.insert(models.UserLiff(user.user_id, line_user_info.sub))
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
            return render_template('error.html', errorId='LC-003', errorStr='内部エラーです。適切な手順でページを開いてください。')
    
    #Lineのリッチメニューの設定

    return render_template('check.html', checkStr='アカウントの連携に成功しました。\nLINEのチャット画面に戻ってください。')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))