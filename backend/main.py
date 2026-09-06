from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



from character import Character

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

character = Character()
@app.get("/api/character")
def get_character():
    return character.get_random_character()

