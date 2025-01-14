from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# データベースから1日の出席状態を取得する関数
def fetch_daily_status(name, start_time, end_time):
    conn = sqlite3.connect('room_status.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT recorded_at, status
        FROM status_history
        WHERE name = ? AND recorded_at BETWEEN ? AND ?
        ORDER BY recorded_at
    ''', (name, start_time, end_time))

    records = cursor.fetchall()
    conn.close()
    return records

def data_processing(records):
    # データの処理（元のロジックをそのまま使用）
    status_by_hour = [0] * 24  # 各時間の在室時間を記録するリスト
    flag = [0] * 12

    for record in records:
        time = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
        hour = time.hour
        minute = time.minute

        #1時間ごとに在籍時間を計測（13時34分なら30分から34分の間は在室していたと判断）
        if record[1] == "在室":
            if (minute in {0, 1, 2, 3, 4}) and (flag[0] != 1):
                status_by_hour[hour] += 5
                flag[0] = 1
            elif (minute in {5, 6, 7, 8, 9}) and (flag[1] != 1):
                status_by_hour[hour] += 5
                flag[1] = 1
            elif (minute in {10, 11, 12, 13, 14}) and (flag[2] != 1):
                status_by_hour[hour] += 5
                flag[2] = 1
            elif (minute in {15, 16, 17, 18, 19}) and (flag[3] != 1):
                status_by_hour[hour] += 5
                flag[3] = 1
            elif (minute in {20, 21, 22, 23, 24}) and (flag[4] != 1):
                status_by_hour[hour] += 5
                flag[4] = 1
            elif (minute in {25, 26, 27, 28, 29}) and (flag[5] != 1):
                status_by_hour[hour] += 5
                flag[5] = 1
            elif (minute in {30, 31, 32, 33, 34}) and (flag[6] != 1):
                status_by_hour[hour] += 5
                flag[6] = 1
            elif (minute in {35, 36, 37, 38, 39}) and (flag[7] != 1):
                status_by_hour[hour] += 5
                flag[7] = 1
            elif (minute in {40, 41, 42, 43, 44}) and (flag[8] != 1):
                status_by_hour[hour] += 5
                flag[8] = 1
            elif (minute in {45, 46, 47, 48, 49}) and (flag[9] != 1):
                status_by_hour[hour] += 5
                flag[9] = 1
            elif (minute in {50, 51, 52, 53, 54}) and (flag[10] != 1):
                status_by_hour[hour] += 5
                flag[10] = 1
            elif (minute in {55, 56, 57, 58, 59}) and (flag[11] != 1):
                status_by_hour[hour] += 5
                flag[11] = 1

    total_presence_time = sum(status_by_hour)
    return status_by_hour, total_presence_time
    #print(status_by_hour)

# メイン画面
@app.route('/')
def index():
    conn = sqlite3.connect('room_status.db')
    cursor = conn.cursor()

    # 最新の状態を取得
    cursor.execute('''
        SELECT name, status, MAX(recorded_at) as last_updated
        FROM status_history
        GROUP BY name
    ''')
    current_status = cursor.fetchall()
    #print(current_status)
    conn.close()

    return render_template('index.html', current_status=current_status)

# 名前をクリックしたときに1日のステータスを取得して表示
@app.route('/status/<name>')
def status(name):
    """
    start_time = datetime.now().strftime('%Y-%m-%d 00:00:00')
    end_time = datetime.now().strftime('%Y-%m-%d 23:59:59')
    """
    today = datetime.now().strftime('%Y-%m-%d')  # 今日の日付 (YYYY-MM-DD形式)
    start_time = f"{today} 00:00:00"
    end_time = f"{today} 23:59:59"

    records = fetch_daily_status(name, start_time, end_time)
    #print(records)

    status_by_hour, total_presence_time = data_processing(records)
    #print(status_by_hour)

    return render_template(
        'status.html',
        name=name,
        date=today,
        statuses=status_by_hour,
        total_presence_time=total_presence_time
    )

@app.route('/status/<name>/<date>')
def date_change(name, date):
    today = datetime.now().strftime('%Y-%m-%d')  # 今日の日付 (YYYY-MM-DD形式)
    start_time = f"{date} 00:00:00"
    end_time = f"{date} 23:59:59"

    records = fetch_daily_status(name, start_time, end_time)
    print(date)

    status_by_hour, total_presence_time = data_processing(records)
    #print(status_by_hour)

    return render_template(
        'status.html',
        name=name,
        today=today,
        date=date,
        statuses=status_by_hour,
        total_presence_time=total_presence_time
    )


if __name__ == '__main__':
    app.run(debug=True)
