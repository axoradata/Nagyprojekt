from typing import Union

from fastapi import FastAPI
from routers import registerUser
from routers import loginUser, logout

from fastapi.middleware.cors import CORSMiddleware # utólag

app = FastAPI()
# -- utólag
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Csak a te frontendet engedi be
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --
app.include_router(registerUser.router)
app.include_router(loginUser.router)
app.include_router(logout.router)

@app.get("/")
async def read_root():
    return {"Hello": "Main World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# fastapi dev main.py