import subprocess

mdb_file = './data_mdb/Finger.mdb'
table_name = 'Absensi'
csv_file = './mytable.csv'

subprocess.run(['mdb-export', mdb_file, table_name], stdout=open(csv_file, 'w'))

