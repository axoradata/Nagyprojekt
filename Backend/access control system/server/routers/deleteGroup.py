from fastapi import APIRouter

from database import query
from moduls import token

router = APIRouter()

token_validator = token.Token()

# delete group
@router.put("/group/delete_group", tags=["group"])
async def delete_group(group_name: str, token: str):
    card_id = token_validator.get_token(token)
    if not card_id or card_id == 'False':
        return {"status": 0, "message": "Érvénytelen token"}

    user_disposition = token_validator.get_disposition(card_id)

    try:
        # ADMIN ÁG
        if user_disposition == 'admin':
            sql_del = f"UPDATE users SET group_name=NULL WHERE group_name='{group_name}';"
            query.insert_into(sql_del)
            return {"status": 1, "message": "Csoport törölve (Admin által)"}

        # EZT A RÉSZT CSERÉLD KI:
        elif user_disposition == 'team_leader':
            # Nem ellenőrizzük, hogy a sajátod-e, ha team_leader vagy, törölheted
            try:
                sql_del = f"UPDATE users SET group_name=NULL WHERE group_name='{group_name}';"
                query.insert_into(sql_del)
                return {"status": 1, "message": "Csoport törölve"}
            except:
                return {"status": 0, "message": "Adatbázis hiba a törlés során"}

        return {"status": 0, "message": "Nincs jogosultság"}

    except Exception as e:
        return {"status": 0, "error": str(e)}