# import requests
# from bs4 import BeautifulSoup

# url = "https://www.curlingzone.com/event.php?eventid=7766&eventtypeid=82&view=Main#1"

# response = requests.get(url)

# soup = BeautifulSoup(response.text, "html.parser")

# print(soup.title.string)  # Print the title of the page

from turtle import title

from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    # url = "https://indianexpress.com/"
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the title of the page
    pagetitle = soup.title.string if soup.title else "No title found"
    title = [];
    for item in soup.find_all("span", class_="titleline"):
        title.append(item.text.strip())


    #Paginate the results
    start = (page - 1) * limit
    end = start + limit
    title = title[start:end]
    
    return {
        "page": page,
        "limit": limit,
        "total": len(title),
        "data": title,
    }
