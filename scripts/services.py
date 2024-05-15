from couchdb.client import Server
from couchdb.http import ResourceNotFound
from datetime import datetime
from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL
from scripts.notes import Note

def convert_creation_date_to_date(note):
    if "creation_date" in note:
        creation_date_str = note["creation_date"]
        creation_date_dt = datetime.strptime(creation_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        note["creation_date"] = creation_date_dt.date()
    return note

def get_all_notes():
    
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    db = server[COUCHDB_DATABASE_NAME]

    mango_query = {
            "selector": {},
            "limit": 100
        }
    
    notes = list(db.find(mango_query))
    
    print(len(notes))

    
    notes = list(db.find(mango_query))
    
    return [convert_creation_date_to_date(note) for note in notes]


def create_database_if_not_exists(server, database_name):
    try:
        server[database_name].info()
    except ResourceNotFound:
        server.create(database_name)

def create_note(title, content, author):
    server = Server(COUCHDB_SERVER_URL)
    create_database_if_not_exists(server, COUCHDB_DATABASE_NAME)
    db = server[COUCHDB_DATABASE_NAME]

    new_note = Note(title=title, content=content, author=author)
    new_note.store(db)
