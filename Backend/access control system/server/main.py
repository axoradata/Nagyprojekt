from typing import Union

from fastapi import FastAPI
from routers import registerUser
from routers import loginUser
from routers import logout
from routers import deleteUser

from routers import registerGroup
from routers import addUserGroup
from routers import deleteUserGroup
from routers import deleteGroup
from routers import userInfo
from routers import getAllUser
from routers import updatePass

from fastapi.middleware.cors import CORSMiddleware

# from routers.updatePass import updatePass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Fejlesztéshez a legegyszerűbb: mindenkit engedélyez
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(registerUser.router)
app.include_router(loginUser.router)
app.include_router(logout.router)
app.include_router(deleteUser.router)
app.include_router(registerGroup.router)
app.include_router(addUserGroup.router)
app.include_router(deleteUserGroup.router)
app.include_router(deleteGroup.router)
app.include_router(userInfo.router)
app.include_router(getAllUser.router)
app.include_router(updatePass.router)
@app.get("/")
async def read_root():
    return {"Hello": "Main World"}


@app.get("/items/")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


#fastapi dev main.py
#1GYdF0S00x01GVed2918hui4xyxd7Dxi6b7SxCSc01xtaBVYc4Pvc0y005bxfxm2