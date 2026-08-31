"""Auth router — register, login, refresh, logout."""
from fastapi import APIRouter,Request
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email:str
    password:str

class SignUpRequest(BaseModel):
    email:str
    password:str
    name:str

def login_controller(req:Request,body:LoginRequest):
    pass
    
    
def signup_controller(req:Request,body:SignUpRequest):
    pass