from datetime import timedelta
from pydantic import BaseModel



class UsersModel(BaseModel):
    card_id: str
    name: str
    password: str
    group_name: str | None
    token: str | None
    token_create_time: timedelta



#####################################################
"""CREATE TABLE IF NOT EXISTS users (
            card_id VARCHAR(32) PRIMARY KEY,
            name VARCHAR(64) NOT NULL,
            password TEXT NOT NULL,
            group_name VARCHAR(64),
            token VARCHAR(64),
            token_create_time TIMESTAMP);"""
#####################################################