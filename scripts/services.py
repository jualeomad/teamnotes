import json
from couchdb.client import Server
from couchdb.http import ResourceNotFound
from datetime import datetime

import requests
from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL
from scripts.notes import Note

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

    requests.post(url, data=index_json, headers={'Content-Type': 'application/json'})


def convert_creation_date_to_date(note):
    if "creation_date" in note:
        creation_date_str = note["creation_date"]
        try:
            creation_date_dt = datetime.fromisoformat(creation_date_str.replace('Z', '+00:00'))
        except ValueError:
            try:
                creation_date_dt = datetime.strptime(creation_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError as e:
                print(f"Error al convertir la fecha: {e}")
                return note
        note["creation_date"] = creation_date_dt.date()
    return note

def get_all_notes(page = 1, page_size = 16):
    # Calculate skip based on page and page_size
    skip = (page - 1) * page_size
    
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    create_sort_notes_by_date_index()
    db = server[COUCHDB_DATABASE_NAME]

    mango_query = {
        "selector": {
            
        },  # Add your specific selector criteria here
        "limit": page_size,
        "skip": skip,
        "sort": [{"creation_date": "desc"}]
    }
    
    notes = list(db.find(mango_query))
    
    is_last_page = len(notes) != page_size
    
    if not is_last_page:
        mango_query["skip"] = page * page_size
        if len(list(db.find(mango_query))) == 0:
            is_last_page = True
    
    return [convert_creation_date_to_date(note) for note in notes], is_last_page

def get_notes_for_user_teams(user_teams, page=1, page_size=16):
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    create_sort_notes_by_date_index()
    db = server[COUCHDB_DATABASE_NAME]

    skip = (page - 1) * page_size

    notes = []
    for team in user_teams:
        mango_query = {
            "selector": {
                "team": team
            },
            "limit": page_size,
            "skip": skip,
        }

        team_notes = db.find(mango_query)
        notes.extend(team_notes)

    is_last_page = len(notes) != page_size
    if not is_last_page:
        mango_query["skip"] = page * page_size
        if len(list(db.find(mango_query))) == 0:
            is_last_page = True

    return [convert_creation_date_to_date(note) for note in notes], len(notes) <= page_size

def create_database_if_not_exists(server, database_name):
    try:
        server[database_name].info()
    except ResourceNotFound:
        server.create(database_name)

def create_note(title, content, author, team):
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    db = server[COUCHDB_DATABASE_NAME]

    new_note = Note(title=title, content=content, author=author, team=team)
    new_note.store(db)
