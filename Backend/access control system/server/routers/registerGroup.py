from fastapi import APIRouter
from models import usersModel

router = APIRouter()

model = usersModel.UsersModel

# create new group
@router.post("/group/register{group_name, username, token}" , tags=["group"])
async def register_group(group_name: model.group_name, username: model.name, token: model.token):
    return {"group": group_name}