import datetime

def create_file_name():
    date = datetime.datetime.now()
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%Y")
    return f"{year}-{month}-{day}.txt"

def get_time():
    date = datetime.datetime.now()
    return date.strftime("%Y-%m-%d %H:%M:%S")

def cerate_log_registration(status:str, data):
    formed_data = result = " ".join(line.strip() for line in data.splitlines())
    if status == 's':
        string_lebght = len(formed_data)
        formed_data = formed_data[2:string_lebght-3]
        return f"Login successful for {formed_data} user"
    elif status == 'd':
        return f"Login failed for {formed_data} card id"
    else:
        return f"Unknown {formed_data}"

def createLog(data:str, status:str):
    file_name = create_file_name()
    time_now = get_time()
    log_smg = cerate_log_registration(status, data)

    try:
        file = open(file_name, "a")
        file.write(f"{time_now} [ {log_smg} ] \n")
        file.close()
        print(f"Server>>> Új bejegyzés a LOG ba {time_now}-kor!")
    except Exception as e:
        print("Server>>> Sikertelen LOG létrehozás!", e)