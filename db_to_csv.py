import pymysql  # Perlu install
from datetime import datetime
import csv
import os
import sys
import shutil

path_data_csv = f'{os.getcwd()}/data_csv'
path_file_csv = f'{os.getcwd()}/data_csv/absensi.csv'
path_file_csv_formatted = f'{os.getcwd()}/data_csv/absensi_formatted.csv'
path_file_log = f'{os.path.abspath(sys.argv[0])[:-2]}log'

time_now = datetime.now().strftime('%d%m%Y %H:%M:%S')

try:
    shutil.rmtree(path_data_csv)
    os.mkdir(path_data_csv)
except Exception as e:
    os.mkdir(path_data_csv)


def writeLog(status, message):
    with open(path_file_log, 'a') as file_log:
        result = f'[{time_now}] {status}: {message}\n'
        file_log.write(result)
        print(result)


def dbToCsv():
    try:
        conn = pymysql.connect(
            host=os.environ.get("IP_MYSQL"),
            port=int(os.environ.get("PORT_MYSQL")),
            user=os.environ.get("USER_MYSQL"),
            password=os.environ.get("PASSWORD_MYSQL"),
            database=os.environ.get("DB_MYSQL")
        )

        cursor = conn.cursor()
        # query = "SELECT * FROM tbl_absensi WHERE status=0 AND LENGTH(nik)=7 ORDER BY id ASC;"
        query = "SELECT * FROM tbl_absensi WHERE status=0 ORDER BY id ASC;"
        cursor.execute(query)

        data = cursor.fetchall()

        with open(path_file_csv, mode='w', newline='') as file_csv:
            penulis_csv = csv.writer(file_csv)
            penulis_csv.writerow([i[0] for i in cursor.description])
            penulis_csv.writerows(data)

        conn.close()

        return True
    except Exception as e:
        writeLog('Error dbToCsv', e)

        return False


def formatCsv():
    if (dbToCsv()):
        try:
            data_input = []
            with open(path_file_csv, mode='r') as file_input:
                csv_reader = csv.reader(file_input)
                next(csv_reader)
                for row in csv_reader:
                    data_input.append(row)

            with open(path_file_csv_formatted, mode='w', newline='') as file_output:
                fieldnames = ['Barcode', 'Nama', 'Date', 'Time']
                writer = csv.DictWriter(file_output, fieldnames=fieldnames)

                writer.writeheader()

                for i, row in enumerate(data_input, start=1):
                    date_time_str = row[2]
                    date_time = datetime.strptime(
                        date_time_str, "%Y-%m-%d %H:%M:%S")
                    barcode = row[1]
                    date = date_time.strftime('%d-%m-%Y')
                    time = date_time.strftime('%H:%M')

                    writer.writerow({'Barcode': barcode, 'Nama': '',
                                    'Date': date, 'Time': time})
            writeLog('Success', 'Get data from DB')
        except Exception as e:
            writeLog('Error formatCsv', e)


formatCsv()
