from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()


@router.post("/user/update_group", tags=["group"])
async def update_user_group(card_id: str, group_name: str, token: str):
    if token_validator.validator(token, ('admin', 'team_leader')):
        try:
            # JAVÍTÁS: 'employee' helyett 'users' tábla kell!
            sql = f"UPDATE users SET group_name='{group_name}' WHERE card_id='{card_id}';"

            # Ez segít neked látni a terminálban, hogy mi történik
            print(f"DEBUG: SQL futtatása -> {sql}")

            query.insert_into(sql)
            return {"status": 1, "message": "Sikeres mentés"}
        except Exception as e:
            print(f"HIBA: {e}")
            return {"status": 0, "error": str(e)}
    return {"status": 0, "message": "Nincs jogosultság"}