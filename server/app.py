from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fastapi.responses import HTMLResponse

from server.routes.quote import router as QuoteRouter


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    # Add any other origins or domains that you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(QuoteRouter, tags=["quotes"], prefix="/quotes")


@app.get("/", tags=["root"])
async def root():
    # read content from ../index.html file
    with open("index.html", "r") as f:
        html = f.read()
    return HTMLResponse(html)
