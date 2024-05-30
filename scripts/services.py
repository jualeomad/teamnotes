import json
from couchdb.client import Server
from couchdb.http import ResourceNotFound
from datetime import datetime

import requests
from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL
from scripts.notes import Note


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

def get_notes_for_user_teams(user_teams, page=1, page_size=16, query='', filter_by='title'):
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    create_sort_notes_by_date_index()
    db = server[COUCHDB_DATABASE_NAME]

    skip = (page - 1) * page_size

    selector = {
        "team": {"$in": user_teams}
    }

    if query:
        if filter_by == 'title':
            selector["title"] = {"$regex": '(?i)' + query}
        elif filter_by == 'author':
            selector["author"] = {"$regex":'(?i)' + query}
        elif filter_by == 'content':
            selector["content"] = {"$regex":'(?i)' + query}

    mango_query = {
        "selector": selector,
        "limit": page_size,
        "skip": skip,
        "sort": [{"creation_date": "desc"}]
    }

    notes = []
    for doc in db.find(mango_query):
        notes.append(doc)

    is_last_page = len(notes) < page_size

    return [convert_creation_date_to_date(note) for note in notes], is_last_page

def create_database_if_not_exists(server, database_name):
    try:
        server[database_name].info()
    except ResourceNotFound:
        server.create(database_name)
        create_sort_notes_by_date_index()

def create_note(title, content, author, team):
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    db = server[COUCHDB_DATABASE_NAME]

    new_note = Note(title=title, content=content, author=author, team=team)
    new_note.store(db)
