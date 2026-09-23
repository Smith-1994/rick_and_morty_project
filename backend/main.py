from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware



#import db_methods
from character import Character
import database_methods

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
    all_character_data = database_methods.get_data(Character._get_total_characters(),character.url)

    database_methods.seed_database(Character.create_statement(), Character.insert_statement(), Character.format_api_response(all_character_data))

    character_data = database_methods.return_data(database_methods.get_random_database_id(Character.get_random_select_statement()),Character.get_character_select_query())
    if character_data is None: 
        raise HTTPException(status_code=404, detail="Character not Found!")

    return(Character.format_data(character_data))


    #db_methods.seed_character_data(db_methods.get_characters_array(), Character.create_table())

    #data = db_methods.return_character_data(db_methods.get_random_database_character_id())
    #if data is None: #Raises an HTTPException if the character is not found in the database
        #raise HTTPException(status_code=404, detail="Character not found")
    #return data




   



if __name__ == "__main__":
    main()
