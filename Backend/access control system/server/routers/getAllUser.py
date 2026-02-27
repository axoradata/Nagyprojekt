from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()
token_validator = token.Token()


@router.get("/user/all", tags=["user"])
async def get_all_users(token: str):
    if token_validator.validator(token, ("admin", "team_leader", "worker")):
        try:
            sql = """
                SELECT e.full_name, e.disposition, e.card_id, u.group_name 
                FROM employee e
                LEFT JOIN users u ON e.card_id = u.card_id;
            """
            users_data = query.select_all(sql)

            results = []
            for user in users_data:
                results.append({
                    "full_name": user[0],
                    "disposition": user[1],
                    "card_id": user[2],
                    "group_name": user[3] if user[3] else None
                })
            return {"status": 1, "users": results}

        except Exception as e:
            return {"status": 0, "error": str(e)}

    return {"status": 0, "message": "Nincs jogosultságod"}