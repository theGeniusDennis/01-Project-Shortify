from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import secrets
import string

app = FastAPI(title="Shortify")


class URLRequest(BaseModel):
    url: HttpUrl


urls = {}


def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def generate_unique_short_code() -> str:
    while True:
        short_code = generate_short_code()

        if short_code not in urls:
            return short_code


@app.post("/api/v1/urls")
def create_short_url(request: URLRequest):
    short_code = generate_unique_short_code()

    urls[short_code] = str(request.url)

    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8000/{short_code}",
        "original_url": str(request.url),
    }


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    original_url = urls.get(short_code)

    if original_url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=original_url,
        status_code=307
    )


@app.get("/")
def root():
    return {"message": "Shortify API is running"}