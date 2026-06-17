from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.notes import router as notes_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

@app.get("/about")
def about():
    return {
        "name": "Robert",
        "learning": "FastAPI"
    }
