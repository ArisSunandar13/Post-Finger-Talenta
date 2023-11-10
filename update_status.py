import csv
import pymysql
import datetime
import os
import sys

path_file_log = f'{os.path.abspath(sys.argv[0])[:-2]}log'

time_now = datetime.datetime.now().strftime('%d%m%Y %H:%M:%S')


def writeLog(status, message):
    with open(path_file_log, 'a') as file_log:
        file_log.write(f'[{time_now}] {status}: {message}\n')


try:
    data_input = []
    with open(f'{os.getcwd()}/data_csv/absensi.csv', mode='r') as file_input:
        csv_reader = csv.reader(file_input)
        next(csv_reader)
        for row in csv_reader:
            data_input.append(row)

    conn = pymysql.connect(
        host=os.environ.get("IP_MYSQL"),
        port=int(os.environ.get("PORT_MYSQL")),
        user=os.environ.get("USER_MYSQL"),
        password=os.environ.get("PASSWORD_MYSQL"),
        database=os.environ.get("DB_MYSQL")
    )

    cursor = conn.cursor()

    # id, nik, tanggal, ip_address, status
    for i, row in enumerate(data_input):
        update_query = f"UPDATE tbl_absensi SET status=1 WHERE id={row[0]};"
        cursor.execute(update_query)
        conn.commit()

    conn.close()

    writeLog('Success', 'Done')
except Exception as e:
    writeLog('Error', e)
