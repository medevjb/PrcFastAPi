from fastapi import FastAPI, Request
from time import time

app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    print(f"Request: {request.method} {request.url} completed in {process_time:.4f} seconds")
    return response




@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # Perform some logic before the request is processed
    print(f"Request URL: next recived {request.url}")
    
    # Call the next middleware or route handler
    response = await call_next(request)
    
    # Perform some logic after the request is processed
    print(f"Response status code: {response.status_code}")
    
    return response