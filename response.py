from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str  # This field will not be included in the response

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

users = [User(id=1, name="John Doe", email="john@example.com", password="secret")]

@app.get("/", response_model=UserResponse)
def get_root():
    return UserResponse(id=1, name="John Doe", email="john@example.com")

@app.get("/users", response_model=UserResponse, status_code=status.HTTP_100_OK)
def get_users():
    return UserResponse(id=1, name="John Doe", email="john@example.com")

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    try:
        # Check if the user already exists
        for existing_user in users:
            if existing_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    users.append(user)
    return UserResponse(id=user.id, name=user.name, email=user.email)