import serial
import time
from dataBase import db_data_in, db_write_log
from log import createLog

ser = serial.Serial('COM5', 115200, timeout=1)

print("Kapcsolódva a Pico-hoz...")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print("Server>>Pico üzenete:", line)
        #response = "PC válasza erre: " + line + "\n"

        response = ''
        if line.startswith('TAG:'):
            data_in_db = db_data_in(line)
            #print(data_in_db)

            if data_in_db != 0:
                response = 'ACK:1' + "\n"
                createLog(data_in_db, 's')
                db_write_log(line)

            elif data_in_db == 0:
                response = 'ACK:0' + "\n"
                createLog(line, 'd')

            time.sleep(0.08)
            ser.write(response.encode('utf-8'))

    time.sleep(0.5)
