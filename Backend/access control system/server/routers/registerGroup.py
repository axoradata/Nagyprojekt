from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# create new group
@router.post("/group/register{group_name, token}" , tags=["group"])
async def register_group(group_name: str, token: str):
    if token_validator.validator(token, ('group_leader','admin',)):
        try:
            sql_query_set = f"""
            UPDATE users SET group_name='{group_name}' WHERE token='{token}';
                            """

            query.insert_into(sql_query_set)

            return {"status": 1}

        except Exception as e:
            return {"status": 0, "error": e}
    else:
        return {"status": 0}