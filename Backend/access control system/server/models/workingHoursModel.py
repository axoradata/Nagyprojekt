from datetime import timedelta
from pydantic import BaseModel



class WorkingHoursModel(BaseModel):
    card_id: str
    token_create_time: timedelta



#####################################################
"""CREATE TABLE IF NOT EXISTS working_hours (
            card_id VARCHAR(32) PRIMARY KEY,
            check_time TIMESTAMP);"""
#####################################################