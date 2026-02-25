from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()

model = usersModel.UsersModel
token_validator = token.Token()

# logout user
@router.post("/user/update", tags=["user"])
async def updatePass(newPass: str, token: str):
    if token_validator.validator(token, ('admin', 'team_leader', 'employee')):
        try:
            # SQL parancs
            sql_query_set = f"UPDATE public.users SET password = '{newPass}' WHERE token = '{token}';"

            # A te kódodban ez a függvény futtatja le a SQL-t:
            query.insert_into(sql_query_set)

            return {"status": 1, "message": "Sikeres frissítés"}

        except Exception as e:
            # Ha itt hiba van, látni fogjuk a JSON válaszban
            return {"status": 0, "error": str(e)}
    return {"status": 0, "message": "Érvénytelen token"}