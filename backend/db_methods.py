import time

import psycopg2
import requests

from character import Character



DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "",
}

char_url = "https://rickandmortyapi.com/api/character/"        

def fetch_character_data():
    first_page = requests.get(char_url)
    first_page.raise_for_status() #Used to check for HTTP error before loop begins
    total_pages = requests.get(char_url).json()['info']['pages']

    all_characters = []
    for current_page in range(1, total_pages + 1):
         
         try: 
            all_characters.extend(_get_page(char_url, current_page))
            time.sleep(0.25)

         except requests.exceptions.RequestException as e:
            print(f"Error fetching character data on page {current_page}: {e}")

    return all_characters  

def _get_page(char_url, page_number, max_retries=3):
    for attempt in range(1, max_retries + 1):

        try:
            response = requests.get(f"{char_url}?page={page_number}")

            if response.status_code == 429:

                wait = response.headers.get("Retry-After") #Check to see if API returns a Retry-After header
                wait = int(wait) if wait and wait.isdigit() else 2 ** attempt #Sets wait to the Retry-After value if it exists, otherwise uses exponential backoff

                print(f"Rate limit exceeded. Waiting for {wait} seconds. Attempt {attempt} of {max_retries}.")

                time.sleep(wait)

                continue

            response.raise_for_status()  #

            return response.json()['results']
        
        except requests.exceptions.RequestException as e:

            print(f"Attempt {attempt} failed for page {page_number}: {e}")

            if attempt == max_retries:

                print(f"Max retries reached for page {page_number}. Skipping.")

                return []  # Return an empty list if all retries fail

def seed_character_data(response):

        # TO FIX: check if table exists and truncate it if exists instead of fully loading it every time

        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS characters (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                status VARCHAR(50),
                species VARCHAR(50),
                type VARCHAR(50),
                gender VARCHAR(50),
                origin VARCHAR(50),
                location VARCHAR(50),
                image VARCHAR(100)
            );
"""
        )

        rows = [
             (character['id'], character['name'], character['status'], character['species'], character['type'], 
              character['gender'], character['origin']['name'], character['location']['name'], character['image'])
             for character in response
        ]
        cursor.executemany(
            """
            INSERT INTO characters (id, name, status, species, type, gender, origin, location, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """,
            rows,
        )

        conn.commit()
        conn.close()
        cursor.close()
        print("Databased seeding finished")

def return_character_data (character_id):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    character = []
    try:

        cursor.execute(
            """
            SELECT * FROM characters WHERE id = (%s);
            """,
            (character_id,),
        )
        character = cursor.fetchone()
        if character is None:
            return None

        return {
            "id": character[0],
            "name": character[1],
            "status": character[2],
            "species": character[3],
            "type": character[4],
            "gender": character[5],
            "origin": character[6],
            "location": character[7],
            "image": character[8],
        }

    #CLoses the connection regardless of whether an exception occurs or not, ensuring that resources are released properly.
    finally:
        cursor.close()
        conn.close()

def get_random_database_character_id():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id FROM characters ORDER BY RANDOM() LIMIT 1;
            """
        )
        row = cursor.fetchone()
        if row is None:

            return None
        
        return row[0]
    
    finally:

        cursor.close()
        conn.close()

def get_characters_array():
    total_characters = Character._fetch_total_characters()
    character_ids = list(range(1, total_characters + 1))

    all_characters = []

    try: 
        all_characters.extend(requests.get(f"{char_url}{character_ids}").json())

    except requests.exceptions.RequestException as e:
        print(f"Error fetching character data: {e}")

    return all_characters

    


