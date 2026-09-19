from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware



import db_methods
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
def main():
    data = db_methods.return_character_data(db_methods.get_random_database_character_id())
    if data is None: #Raises an HTTPException if the character is not found in the database
        raise HTTPException(status_code=404, detail="Character not found")
    return data

   



if __name__ == "__main__":
    main()
