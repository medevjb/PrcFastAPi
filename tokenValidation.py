from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel

app = FastAPI()

def verify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return {
        "user": "Authorized User",
        "token": token
    }

@app.get("/secure-data")
def get_secure_data(auth: dict = Depends(verify_token)):
    return {"message": "This is secure data", "user": "user"} # Static user info, can be replaced with dynamic user info based on token
    return {"message": "This is secure data", "user": auth["user"]} # dynamic user info based on token

