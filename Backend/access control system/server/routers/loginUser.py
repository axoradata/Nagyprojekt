from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()

model = usersModel.UsersModel
token_validator = token.Token()

# login user
@router.post("/user/login{username, password}" , tags=["user"])
async def login(username: str, password: str):
    try:
        sql_query_users = f"""
                        SELECT disposition FROM employee FULL JOIN users ON users.card_id = employee.card_id WHERE name='{username}' AND password='{password}';
                        """

        data = query.select(sql_query_users)

        if data:
            new_token = token_validator.create_token()
            sql_query_set = f"""
                            UPDATE users SET token='{new_token}' WHERE name='{username}';
                            """

            query.insert_into(sql_query_set)
            return {"status": 1, "token": new_token, "disposition": data}
        else:
            return {"status": 0}

    except Exception as e:
        return {"status": 0, "error": e}