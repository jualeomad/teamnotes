from couchdb.client import Server
import json
import sys
import os
import requests

# Add the parent directory of 'teamnotes' to the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from scripts.services import convert_creation_date_to_date
from scripts.notes import Note
from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL


# Necesario para hacer el sort directamente en query de couchdb
# y no ordenarlo con python posterior a la query
def create_sort_notes_by_date_index():
    # Definir los datos del índice
    index_data = {
    "index": {
        "fields": [
            "creation_date"
        ]
    },
    "name": "notes-sorted-by-creation-date",
    "type": "json"
    }
    
    index_json = json.dumps(index_data)

    url = COUCHDB_SERVER_URL + '/' + COUCHDB_DATABASE_NAME + '/_index'

    response = requests.post(url, data=index_json, headers={'Content-Type': 'application/json'})

    print("Error al crear el índice:", response.status_code)
    print(response.text)


if __name__=='__main__':

    server = Server(COUCHDB_SERVER_URL)
    db = server[COUCHDB_DATABASE_NAME]

    create_sort_notes_by_date_index()

    populate_file = 'MOCK_DATA.json'

    print(db.index()._list())

    db.index()

    with open(populate_file, 'r', encoding="utf-8") as file:
        # Load JSON data from the file
        json_data = json.load(file)
        for note in json_data:
            new_note = convert_creation_date_to_date(note)
            new_note = Note(title=note["title"], content=note["content"], creation_date=note["creation_date"], author=note["author"])
            new_note.store(db)
