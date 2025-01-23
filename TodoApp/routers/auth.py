from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext
from models import Users

router = APIRouter()

# Initialize password hashing context
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Input schema for user creation
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.post('/auth')
def create_user(create_user_request: CreateUserRequest):
    user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt.hash(create_user_request.password),  
        is_active=True  
    )

    return user_model