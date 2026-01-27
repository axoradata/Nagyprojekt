from fastapi import APIRouter
from models import usersModel

from database import query
from moduls import token

router = APIRouter()

model = usersModel.UsersModel
token_validator = token.Token()

# logout user
@router.post("/user/logout{token}" , tags=["user"])
async def logout(token: str):
    if token_validator.get_token(token):
        try:
            sql_query_set = f"""
            UPDATE users SET token=null WHERE token='{token}';
                                """

            query.insert_into(sql_query_set)
            return {"status": 1}

        except Exception as e:
            return {"status": 0, "error": e}
    else:
        return {"status": 0}