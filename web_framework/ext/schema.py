"""Base data models"""
from typing import Dict, Any, Optional

from pydantic import BaseModel


class BaseRequest(BaseModel):
    """
    Base request data model.
    NOTE: Inherit this class to add specific fields from request,
    needed in view
    """
    method: str
    params: Dict[str, Any]
    body: Optional[Dict[str, Any]]
