from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

def common_logic():
    # This function can contain common logic that you want to apply to multiple endpoints
    # For example, you can check for authentication, logging, etc.
    # Here, we will just return a simple message for demonstration purposes
    return {"message": "Common logic executed"}

@app.get("/home")
def home(data = Depends(common_logic)):
    return data;