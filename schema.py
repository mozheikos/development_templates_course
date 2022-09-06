"""
Module define dataclasses
"""


from pydantic import BaseModel, validator


class AccountInfo(BaseModel):
    """Account data model"""

    id: str
    acc_type_name: str
    balance: float = 0.0
    code_hash: str
    data_hash: str

    @validator('balance', pre=True)
    def get_balance(cls, value: str) -> float:
        """Converts blockchain account balance to real EVER"""
        return int(value) / 10**9
