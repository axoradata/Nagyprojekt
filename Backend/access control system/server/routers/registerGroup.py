from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# create new group
@router.post("/group/register")
async def register_group(group_name: str, token: str, leader_card_id: str = None):
    # 1. Ki hozza létre?
    creator_card_id = token_validator.get_token(token)
    creator_disposition = token_validator.get_disposition(creator_card_id)

    try:
        if creator_disposition == 'admin':
            if not leader_card_id:
                return {"status": 0, "message": "Adminnak kötelező csoportvezetőt választani!"}

            sql = f"UPDATE users SET group_name='{group_name}' WHERE card_id='{leader_card_id}';"
            query.insert_into(sql)
            return {"status": 1, "message": f"Csoport létrehozva, vezető kinevezve."}

        elif creator_disposition == 'team_leader':
            sql = f"UPDATE users SET group_name='{group_name}' WHERE card_id='{creator_card_id}';"
            query.insert_into(sql)
            return {"status": 1, "message": "Csoport létrehozva, ön a vezetője."}

        return {"status": 0, "message": "Nincs jogosultság"}

    except Exception as e:
        return {"status": 0, "error": str(e)}