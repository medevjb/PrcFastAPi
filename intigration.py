#Basic integration with external API using FastAPI and requests library
# from fastapi import FastAPI
# import requests
# from config import config 

# app = FastAPI()

    
# POSTS = config.API_ROOT+"/posts"
# response = requests.get(POSTS)

# data = response.json()
# print(data[:2])


#Throught FastAPI
from fastapi import FastAPI, HTTPException
import requests
from config import config

app = FastAPI()

@app.get("/")
def posts():
    url = config.API_ROOT + "/posts"
    response = requests.get(url)
    if response.status_code != 200:
       raise HTTPException(status_code=500, detail="Failed to fetch posts")
    data = response.json()
    return data[:2]


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    url = config.API_ROOT + f"/posts/{post_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch post")
    data = response.json()
    return data


