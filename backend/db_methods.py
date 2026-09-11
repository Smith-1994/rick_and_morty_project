import psycopg2
import requests

DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "rm_database",
    "user": "postgres",
    "password": "postgres",
}
        

def fetch_character_data():
    try: 
        response = requests.get("https://rickandmortyapi.com/api/character/")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching character data: {e}")
        return []  

def insert_character_data(response):


        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS characters (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                status VARCHAR(50),
                species VARCHAR(50),
                type VARCHAR(50),
                gender VARCHAR(50)
            );
"""
        )

        rows = [
             (character['name'], character['status'], character['species'], character['type'], character['gender'])
             for character in response['results']
        ]
        cursor.executemany(
            """
            INSERT INTO characters (name, status, species, type, gender)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )

        conn.commit()
        cursor.close()


 


