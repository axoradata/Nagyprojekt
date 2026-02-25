from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()

model = usersModel.UsersModel
token_validator = token.Token()

# login user
@router.post("/user/login" , tags=["user"])
async def login(username: str, password: str):
    try:
        sql_query_users = f"""
            SELECT users.card_id, employee.disposition, employee.full_name 
            FROM users 
            JOIN employee ON users.card_id = employee.card_id 
            WHERE users.name='{username}' AND users.password='{password}';
        """

        data = query.select(sql_query_users)

        if data:
            new_token = token_validator.create_token()
            sql_query_set = f"""
                            UPDATE users SET token='{new_token}' WHERE name='{username}';
                            """

            query.insert_into(sql_query_set)
            return {"status": 1, "token": new_token, "card_id": data[0], "role": data[1],  "name": data[2]}
        else:
            return {"status": 0}

    except Exception as e:
        return {"status": 0, "error": e}