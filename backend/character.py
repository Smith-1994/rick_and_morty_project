import requests
import json
import random

class Character: 
    def __init__(self):
        pass

        # This function generates a random number between 1 and the total number of characters in the Rick and Morty API
    def _gen_random_number(self):
        totalCharacters = requests.get("https://rickandmortyapi.com/api/character").json()['info']['count']
        return random.randint(1, totalCharacters)

        # This function fetches a random character from the Rick and Morty API and prints the character's data in a formatted JSON structure
    def get_random_character(self):
        data = requests.get(f"https://rickandmortyapi.com/api/character/{self._gen_random_number()}").json()
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
