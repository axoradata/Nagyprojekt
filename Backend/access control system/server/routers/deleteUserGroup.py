from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# remove group member
@router.put("/group/delete_member" , tags=["group"])
async def delete_group_member(username: str, token: str):
    if token_validator.validator(token, ('admin', 'group_leader',)):
        group_name = ''
        sql_query_get_name = f"""
                       SELECT group_name FROM USERS WHERE token='{token}';
                                       """
        data = query.select(sql_query_get_name)
        if data:
            group_name = data[0]
        else:
            return {"status": 0}

        try:
            sql_query_set = f"""
               UPDATE users SET group_name=null WHERE name='{username}';
                               """

            query.insert_into(sql_query_set)

            return {"status": 1}

        except Exception as e:
            return {"status": 0, "error": e}
    else:
        return {"status": 0}