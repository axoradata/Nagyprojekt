import datetime

from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# get user information souch as working hour & group info etc...
@router.get("/user/info" , tags=["user"])
async def user_info(token: str):
    if token_validator.validator(token, ('admin', 'team_leader', 'employee')):
        # 1. Alapadatok lekérése a USERS táblából
        sql_user = f"SELECT group_name, card_id FROM USERS WHERE token='{token}';"
        user_data = query.select(sql_user)

        if not user_data:
            return {"status": 0, "message": "User not found"}

        group_name = user_data[0] if user_data[0] else 'None'
        card_id = user_data[1]

        # 2. Részletes adatok az employee táblából
        sql_emp = f"SELECT full_name, disposition FROM employee WHERE card_id='{card_id}';"
        emp_data = query.select(sql_emp)
        full_name = emp_data[0] if emp_data else "Ismeretlen"
        disposition = emp_data[1] if emp_data else "worker"

        # 3. Munkalap adatok lekérése (Minden log, időrendben)
        # Itt formázzuk a dátumot SQL szinten vagy Pythonban, hogy ne legyen benne 'T'
        sql_work = f"SELECT check_time FROM working_hours WHERE card_id='{card_id}' ORDER BY check_time ASC;"
        raw_working_hours = query.select_all(sql_work)

        # Átalakítás string listává: "2026. 02. 02. 08:00:00" formátumra
        # Ez pontosan az, amit a frontend parseLogTime függvényed vár!
        formatted_hours = []
        if raw_working_hours:
            for row in raw_working_hours:
                dt = row[0]  # feltételezve, hogy datetime objektum
                if isinstance(dt, datetime.datetime):
                    formatted_hours.append(dt.strftime("%Y.%m.%d. %H:%M:%S"))
                else:
                    # Ha már stringként jönne az adatbázisból
                    formatted_hours.append(str(dt).replace('-', '.').replace('T', ' '))

        return {
            "status": 1,
            "group": group_name,
            "working_hours": formatted_hours,  # Ez a lista megy a frontendnek
            "card_id": card_id,
            "disposition": disposition,
            "full_name": full_name
        }

    return {"status": 0, "message": "Invalid token"}