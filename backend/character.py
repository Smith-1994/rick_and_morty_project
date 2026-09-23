import requests
import json
import random
import redis


class Character: 
    #redis_client = redis.Redis(host='localhost', port=6379, db=0)
    #CACHE_KEY = "rick_and_morty_character_cache"
    #CACHE_TTL = 60 * 60 * 24  # Cache for 24 hours


    def __init__(self):
        self._url = "https://rickandmortyapi.com/api/character/"

    @property
    def url(self):
        return self._url



        # This function fetches the total number of characters in the Rick and Morty API and caches the result in Redis for 24 hours
    @staticmethod
    def _get_total_characters():

        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        CACHE_KEY = "rick_and_morty_character_cache"
        CACHE_TTL = 60 * 60 * 24  # Cache for 24 hours

        cached_count = redis_client.get(CACHE_KEY)

        if cached_count:
            print("Cache HIT, returning cached value")
            return int(cached_count)
        else:
            total_characters = requests.get('https://rickandmortyapi.com/api/character/').json()['info']['count']
            redis_client.setex(name=CACHE_KEY, time=CACHE_TTL, value=total_characters)
            print("Cache MISS, fetching from API and caching the value")
            return total_characters


    #Returns create table statement for characters table
    def create_statement():
        return(
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

    #Response is recieved from database_methods.get_data
    def insert_statement():

        return(
                """
            INSERT INTO characters (id, name, status, species, type, gender, origin, location, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
        )

    #returns a random ID from character table
    def get_random_select_statement():
        return(
                        """
            SELECT id FROM characters ORDER BY RANDOM() LIMIT 1;
            """
        )

    #Returns data from a select query
    def get_character_select_query():
        return ("""
            SELECT * FROM characters WHERE id = (%s);
            """
        )

    #Formats data from SQL select query to JSON
    #This formatted data gets sent to the front end
    def format_data(data):
        return (
                {
                    "id": data[0],
                    "name": data[1],
                    "status": data[2],
                    "species": data[3],
                    "type": data[4],
                    "gender": data[5],
                    "origin": data[6],
                    "location": data[7],
                    "image": data[8],
                }
        )















        # This function generates a random number between 1 and the total number of characters in the Rick and Morty API
    def _gen_random_number(self):
        totalCharacters = self._fetch_total_characters()
        return random.randint(1, totalCharacters)

        # This function fetches a random character from the Rick and Morty API and prints the character's data in a formatted JSON structure
    def get_random_character_from_api(self):
        data = requests.get(f"{self.character_url}{self._gen_random_number()}").json()
        return{
            "id": data['id'],
            "name": data['name'],
            "status": data['status'],
            "species": data['species'],
            "type": data['type'],
            "gender": data['gender'],
            "origin": data['origin'],
            "location": data['location'],
            "image": data['image'],
        }

    def get_select_character_from_api(self, character_id):
        data = requests.get(f"{self.character_url}{character_id}").json()
        return{
            "id": data['id'],
            "name": data['name'],
            "status": data['status'],
            "species": data['species'],
            "type": data['type'],
            "gender": data['gender'],
            "origin": data['origin'],
            "location": data['location'],
            "image": data['image'],
        }
