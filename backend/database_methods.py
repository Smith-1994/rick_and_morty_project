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


#Accepts a create table and insert table statement from characters/episodes/locations
#Seeds corresponding database
def seed_database(create_table_statement, insert_table_statement, rows):

        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute(create_table_statement)

        cursor.executemany(insert_table_statement, rows,)

        conn.commit()
        conn.close()
        cursor.close()
        print("Databased seeding finished")



#Accepts a select statement from character/episode/location
#Returns a random ID from corresponding database
def get_random_database_id(random_select_statement):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    try:
        cursor.execute(random_select_statement)
        row = cursor.fetchone()
        if row is None:

            return None
        
        return row[0]
    
    finally:

        cursor.close()
        conn.close()


#Accepts total number of data elements and url from characters/episodes/locations
#Pulls data from API using an array method
#Returns full response from API in JSON format 
def get_data(total_elements, url):
    ids = list(range(1, total_elements + 1))

    response = []

    try: 
        response.extend(requests.get(f"{url}{ids}").json())

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    #Returns response from API
    return response

    
#Accepts an id number (or randomly generated number from method)
#Accepts select query from characters/episodes/locations
#Returns data from SQL as an array of data for one element
def return_data (id, select_statement):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    data = []
    try:

        cursor.execute(
            (select_statement),
            (id,),
        )
        data = cursor.fetchone()
        if data is None:
            return None

        return data

    #CLoses the connection regardless of whether an exception occurs or not, ensuring that resources are released properly.
    finally:
        cursor.close()
        conn.close()






#Everything below this comment has not been updated



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


