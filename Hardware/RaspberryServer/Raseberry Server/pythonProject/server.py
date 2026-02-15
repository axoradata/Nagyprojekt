import serial
import time
import sqlite3

COM_PORT = 'COM5'    # ha más port, cseréld
BAUD = 115200        # a Pico USB CDC-hez elég ez (PC oldalon a baud csak a terminálokhoz releváns)
TIMEOUT = 1

def data_formating(data:str):
    formed_data = data.replace('TAG:', '')
    return formed_data

def db_data_in(card_id):
    try:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        data = data_formating(card_id)

        res = cur.execute(f"SELECT name FROM employee WHERE card_id='{data}'")
        response = res.fetchone()

        if response is not None:
            return 1
        else:
            return 0
    except Exception as e:
        print("Adat hiba //data_is_init// function", e)
        return 0

def main():
    try:
        ser = serial.Serial(COM_PORT, BAUD, timeout=TIMEOUT)
    except Exception as e:
        print("Nem sikerült megnyitni a COM portot:", e)
        return

    print("Kapcsolódva:", COM_PORT)
    try:
        while True:
            try:
                raw = ser.readline()  # newline-ig olvas
                if not raw:
                    continue
                line = raw.decode('utf-8', errors='replace').strip()
                print("FROM PICO:", line)

                # példa: ha TAG: kezdetet kapunk, küldjünk ACK-et vissza
                if line.startswith('TAG:'):

                    print(db_data_in(line))
                    # ACK küldése
                    ser.write(b'ACK\n')
                    print("ACK elküldve")

                time.sleep(0.05)
            except Exception as e:
                print("Olvasási hiba:", e)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Kilépés...")
    finally:
        ser.close()
