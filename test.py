import sqlite3
from datetime import datetime

# データベースとテーブルを作成する関数
def create_database():
    conn = sqlite3.connect('room_status.db')  # データベースファイルを作成
    cursor = conn.cursor()

    # 現在のステータスを記録するテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_status (
            name TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            updated_at DATETIME NOT NULL
        )
    ''')

    # ステータスの履歴を記録するテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            recorded_at DATETIME NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# サンプルデータをデータベースに挿入する関数
def insert_sample_data():
    conn = sqlite3.connect('room_status.db')
    cursor = conn.cursor()

    sample_data = [
        {"name": "山田太郎", "status": "在室", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {"name": "鈴木花子", "status": "在室", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {"name": "田中博", "status": "退室", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},

    ]

    for record in sample_data:
        # current_statusテーブルを更新
        cursor.execute('''
            INSERT INTO current_status (name, status, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                status = excluded.status,
                updated_at = excluded.updated_at
        ''', (record["name"], record["status"], record["time"]))

        # status_historyテーブルに履歴を挿入
        cursor.execute('''
            INSERT INTO status_history (name, status, recorded_at)
            VALUES (?, ?, ?)
        ''', (record["name"], record["status"], record["time"]))

    conn.commit()
    conn.close()

# データベースからデータをリストに取り出す関数
def fetch_data_to_list():
    conn = sqlite3.connect('room_status.db')
    cursor = conn.cursor()

    current_status_list = []
    status_history_list = []

    # current_statusテーブルからデータを取り出しリストに格納
    cursor.execute('SELECT * FROM current_status')
    for row in cursor.fetchall():
        current_status_list.append({
            "name": row[0],
            "status": row[1],
            "updated_at": row[2]
        })

    # status_historyテーブルからデータを取り出しリストに格納
    cursor.execute('SELECT * FROM status_history')
    for row in cursor.fetchall():
        status_history_list.append({
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "recorded_at": row[3]
        })

    conn.close()

    return current_status_list, status_history_list


# 名前と指定された時間範囲でデータを取得し表示する関数
def fetch_records_by_name_and_time(name, start_time):
    conn = sqlite3.connect('room_status.db')
    cursor = conn.cursor()

    # SQLクエリで条件を指定してデータを取得
    cursor.execute('''
        SELECT * FROM status_history
        WHERE name = ? AND recorded_at >= ?
    ''', (name, start_time))

    # 取得したデータをリストに格納
    records = []
    for row in cursor.fetchall():
        records.append({
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "recorded_at": row[3]
        })

    conn.close()

    # 結果を表示
    print(f"=== Records for {name} from {start_time} to now ===")
    for record in records:
        print(record)

    #print(records)

# データを表示する関数
def display_data():
    current_status_list, status_history_list = fetch_data_to_list()

    print("=== Current Status ===")
    for entry in current_status_list:
        print(entry)

    print("\n=== Status History ===")
    for entry in status_history_list:
        print(entry)

def clear_table():
    # データベースに接続
    conn = sqlite3.connect('room_status.db')
    cursor = conn.cursor()

    # テーブルのデータを削除
    cursor.execute('DELETE FROM status_history')

    # 変更を保存
    conn.commit()
    print("テーブル 'room_status' の中身をクリアしました。")

    # 接続を閉じる
    conn.close()

#テーブル一覧表示
def list_tables(db_path):
    try:
        # SQLiteデータベースに接続
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # テーブル一覧を取得するクエリ
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # テーブル名のリストを表示
        print("Tables in the database:")
        for table in tables:
            print(table[0])
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # 接続を閉じる
        if connection:
            connection.close()


# メイン処理
if __name__ == '__main__':
    #create_database()        # データベースとテーブルを作成
    insert_sample_data()     # サンプルデータをデータベースに挿入

    list_tables('room_status.db')

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 指定された開始時刻
    start_time = '2024-11-28 16:45:00'
    # 名前を指定してデータを取得
    #clear_table()
    #fetch_records_by_name_and_time("田中博", start_time)


    #display_data()           # データベースからデータをリストに取り出して表示
