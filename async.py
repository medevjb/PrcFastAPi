import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

# def task():
#     print("Task started")
#     time.sleep(2)
#     print("Task completed")

# async def async_task():
#     print("Async task started")
#     await asyncio.sleep(2)
#     print("Async task completed")



@app.get("/sync-task")
async def sync_task():
    print("Sync task started")
    await asyncio.sleep(2)
    print("Sync task completed")
    return {"message": "Sync task completed"}


