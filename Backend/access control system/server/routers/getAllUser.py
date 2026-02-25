from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()
token_validator = token.Token()

@router.get("/user/all", tags=["user"])
async def get_all_users(token: str):
    if token_validator.validator(token, ("admin",)):

        sql = "SELECT full_name, disposition, card_id FROM employee;"
        users_data = query.select_all(sql)

        # frontendnek lista
        results = []
        for user in users_data:
            results.append({
                "full_name": user[0],
                "disposition": user[1],
                "card_id": user[2]
            })
        return {"status": 1, "users": results}
    return {"status": 0, "message": "Nincs jogosultságod"}