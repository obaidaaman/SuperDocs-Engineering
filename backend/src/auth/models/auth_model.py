from typing import Optional
from pydantic import BaseModel, Field


class Login(BaseModel):
    email : str
    password : str


class Register(BaseModel):
    email : str
    password : str
    first_name : str
    last_name : str
    phone : str
    # If the user is joining an existing organization
    org_id : Optional[int] = None
    # If the user is creating a new organization
    org_name : Optional[str] = None


