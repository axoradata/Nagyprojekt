from fastapi import APIRouter
from models import employeeModel

router = APIRouter()

model = employeeModel.EmployeeModel

# delete user
@router.delete("/user/delete{card_id, token}" , tags=["admin"])
async def delete(card_id: model.card_id, token: str):
    return {"employee": card_id}