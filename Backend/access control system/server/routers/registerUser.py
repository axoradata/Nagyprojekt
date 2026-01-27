from fastapi import APIRouter
from models import employeeModel

from database import query
from moduls import token

router = APIRouter()

model = employeeModel.EmployeeModel
token_validator = token.Token()

# register new user
@router.post("/user/register{card_id, disposition, full_name, user_name, password, token}" , tags=["admin"])
async def register(card_id:str, disposition:str, full_name:str, user_name:str, password:str, token:str):
    if token_validator.validator(token, ('admin',)):
        try:
            sql_query_employee = f"""
            INSERT INTO employee (card_id, disposition, full_name, first_day) VALUES ('{card_id}', '{disposition}', '{full_name}', '2026-01-08');
            """

            sql_query_users = f"""
                    INSERT INTO users (card_id, name, password, group_name, token, token_create_time) VALUES ('{card_id}', '{user_name}', '{password}', NULL, NULL, NULL);
                    """

            query.insert_into(sql_query_employee)
            query.insert_into(sql_query_users)

            return {"status": 1}

        except Exception as e:
            return {"status": 0, "error": e}
    else:
        return {"status": 0}