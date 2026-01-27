from fastapi import APIRouter
from models import employeeModel

from database import query
from moduls import token

router = APIRouter()

model = employeeModel.EmployeeModel
token_validator = token.Token()

# delete user
@router.delete("/user/delete{card_id, token}" , tags=["admin"])
async def delete(card_id: str, token: str):
    if token_validator.validator(token, ('admin',)):
        try:
            sql_query_set = f"""
            DELETE FROM users WHERE card_id='{card_id}';
                            """
            query.insert_into(sql_query_set)

            sql_query_set = f"""
            DELETE FROM employee WHERE card_id='{card_id}';
                            """
            query.insert_into(sql_query_set)

            return {"status": 1}

        except Exception as e:
            return {"status": 0, "error": e}
    else:
        return {"status": 0}