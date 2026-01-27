import datetime

from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# get user information souch as working hour & group info etc...
@router.get("/user/info{token}" , tags=["user"])
async def user_info(token: str):
    if token_validator.validator(token, "abrakadabra"):
        working_hours = ''
        group_name = ''
        card_id = ''

        sql_query_get_name = f"""
                            SELECT group_name FROM USERS WHERE token='{token}';
                            """
        group_data = query.select(sql_query_get_name)
        if group_data:
            group_name = group_data[0]
        else:
            group_name = 'None'


        sql_query_get_card_id = f"""
                                   SELECT card_id FROM USERS WHERE token='{token}';
                                """
        card_data = query.select(sql_query_get_card_id)
        if card_data:
            card_id = card_data[0]

            current_time = datetime.datetime.now()
            now_time = f"{current_time.year}-{current_time.month}-{current_time.day} 00:00:00"

            sql_query_get_work = f"""
                                       SELECT check_time FROM working_hours WHERE card_id='{card_id}' AND check_time >= '{now_time}';
                                    """
            working_hours = query.select_all(sql_query_get_work)
            return {"status": 1, "group": group_name, "working_hours": working_hours}

        else:
            return {"status": 0}

    else:
        return {"status": 0}