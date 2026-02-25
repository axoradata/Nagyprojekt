from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# delete group
@router.put("/group/delete_group" , tags=["group"])
async def delete_group(token: str):
    if token_validator.validator(token, ('admin', 'group_leader',)):
        group_name = ''
        sql_query_get_name = f"""
                    SELECT group_name FROM USERS WHERE token='{token}';
                                    """
        get_data = query.select(sql_query_get_name)
        if get_data:
            group_name = get_data[0]
        else:
            return {"status": 0}

        sql_query_all_name = f"""
                    SELECT name FROM USERS WHERE group_name='{group_name}';
                                    """

        datas = query.select_all(sql_query_all_name)

        for i in datas:
            str_data = str(i)
            leng = len(str_data) - 3
            clean_data = str_data[2:leng]

            try:
                sql_query_set = f"""
                UPDATE users SET group_name=null WHERE name='{clean_data}';
                                """

                query.insert_into(sql_query_set)

            except Exception as e:
                return {"status": 0, "error": e}

        return  {"status": 1}

    else:
        return {"status": 0}