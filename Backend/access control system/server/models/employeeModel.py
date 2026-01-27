from datetime import date
from pydantic import BaseModel



class EmployeeModel(BaseModel):
    card_id: str
    disposition: str
    full_name: str
    first_day: date



#####################################################
"""CREATE TABLE IF NOT EXISTS employee (
            card_id VARCHAR(32) PRIMARY KEY,
            disposition VARCHAR(16) NOT NULL,
            full_name TEXT NOT NULL,
            first_day DATE NOT NULL);"""
#####################################################