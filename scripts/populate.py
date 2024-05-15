from couchdb.client import Server
import json

import sys
import os


# Add the parent directory of 'teamnotes' to the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from scripts.services import convert_creation_date_to_date
from scripts.notes import Note
from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL


server = Server(COUCHDB_SERVER_URL)
db = server[COUCHDB_DATABASE_NAME]

populate_file = 'MOCK_DATA.json'

with open(populate_file, 'r') as file:
    # Load JSON data from the file
    json_data = json.load(file)
    for note in json_data:
        new_note = convert_creation_date_to_date(note)
        new_note = Note(title=note["title"], content=note["content"], creation_date=note["creation_date"], author=note["author"])
        new_note.store(db)
    