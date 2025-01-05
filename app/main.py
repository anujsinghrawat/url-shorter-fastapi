from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string, random

app = FastAPI()

# In-memory database: { "short_id": "original_url" }
url_db = {}

# Pydantic model for request body
class URLRequest(BaseModel):
    url: str
    
@app.get("/")
def read_root():
    return {"message": "Welcome to URL shortener service"}

def generate_short_id(length=6):
    # Generate a random string of given length
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@app.post("/shorten")
def shorten_url(url_request: URLRequest):
    # Generate a unique short ID that is not already used
    short_id = generate_short_id()
    while short_id in url_db:
        short_id = generate_short_id()

    url_db[short_id] = url_request.url
    return {"short_url": f"/{short_id}"}

@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    if short_id not in url_db:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": url_db[short_id]}
