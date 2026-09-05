import requests
import json
import random
import time
import redis

class Character: 
    character_url = "https://rickandmortyapi.com/api/character/"

    def __init__(self):
        pass

        # This function generates a random number between 1 and the total number of characters in the Rick and Morty API
    def _gen_random_number(self):
        totalCharacters = requests.get(self.character_url).json()['info']['count']
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
