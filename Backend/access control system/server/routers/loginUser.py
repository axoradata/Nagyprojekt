from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()

model = usersModel.UsersModel
token_validator = token.Token()

# login user
@router.post("/user/login", tags=["user"])      # az axios nem tudta kezelni a kapcsos részt
async def login(username: str, password: str):
    try:
        sql_query_users = f"""
                        SELECT card_id FROM users WHERE name='{username}' AND password='{password}'
                        """

        data = query.select(sql_query_users)

        if data:        # generálja és menti az adatbázisba a bejelentkezéskor a tokent
            new_token = token_validator.create_token()
            sql_update = f"UPDATE users SET token='{new_token}' WHERE name='{username}'"
            query.insert_into(sql_update)
            return {"status": 0, "token": token_validator.create_token()}
        else:
            return {"status": 0}

    except Exception as e:
        return {"status": 0, "error": e}