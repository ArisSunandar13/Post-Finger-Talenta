import csv
from datetime import datetime

# Baca data dari file CSV
data_input = []
with open('./mytable.csv', mode='r') as file_input:
    csv_reader = csv.reader(file_input)
    next(csv_reader)  # Lewati baris header
    for row in csv_reader:
        data_input.append(row)

# Membuka file CSV untuk menulis hasil
with open('output.csv', mode='w', newline='') as file_output:
    fieldnames = ['Barcode', 'Nama', 'Date', 'Time']
    writer = csv.DictWriter(file_output, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for i, row in enumerate(data_input, start=1):
        date_time_str = row[0]
        date_time = datetime.strptime(date_time_str, "%m/%d/%y %H:%M:%S")
        barcode = row[row.__len__()-1]
        date = date_time.strftime('%m-%d-%Y')
        time = date_time.strftime('%H:%M')
        
        writer.writerow({'Barcode': barcode, 'Nama': '', 'Date': date, 'Time': time})

print("Data telah diubah dan disimpan dalam file 'output.csv'.")
