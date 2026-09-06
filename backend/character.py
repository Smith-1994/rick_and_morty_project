import requests
import json
import random
import time
import redis

class Character: 
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    character_url = "https://rickandmortyapi.com/api/character/"
    CACHE_KEY = "rick_and_morty_character_cache"
    CACHE_TTL = 60 * 60 * 24  # Cache for 24 hours

    def __init__(self):
        pass

        # This function fetches the total number of characters in the Rick and Morty API and caches the result in Redis for 24 hours
    def _fetch_total_characters(self):
        cached_count = self.redis_client.get(self.CACHE_KEY)
        if cached_count:
            return int(cached_count)
        else:
            total_characters = requests.get(self.character_url).json()['info']['count']
            self.redis_client.setex(name=self.CACHE_KEY, time=self.CACHE_TTL, value=total_characters)
            return total_characters

        # This function generates a random number between 1 and the total number of characters in the Rick and Morty API
    def _gen_random_number(self):
        totalCharacters = self._fetch_total_characters()
        return random.randint(1, totalCharacters)

        # This function fetches a random character from the Rick and Morty API and prints the character's data in a formatted JSON structure
    def get_random_character(self):
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
