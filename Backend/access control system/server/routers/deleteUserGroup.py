from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# remove group member
@router.put("/group/delete_member", tags=["group"])
async def delete_group_member(card_id: str, token: str):

    if token_validator.validator(token, ('admin', 'team_leader')):
        try:
            sql_query_set = f"""
                UPDATE users SET group_name = NULL WHERE card_id = '{card_id}';
            """
            query.insert_into(sql_query_set)

            return {"status": 1}

        except Exception as e:
            return {"status": 0, "error": str(e)}

    else:
        return {"status": 0, "message": "Nincs jogosultság"}