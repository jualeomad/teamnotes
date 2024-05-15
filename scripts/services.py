
from couchdb.client import Server
from datetime import datetime

from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL

def convert_creation_date_to_date(note):
    if "creation_date" in note:
        creation_date_str = note["creation_date"]
        # Convertir la cadena a objeto datetime
        creation_date_dt = datetime.fromisoformat(creation_date_str)
        # Extraer solo la fecha del objeto datetime
        note["creation_date"] = creation_date_dt.date()
    return note


def get_all_notes():
    server = Server(COUCHDB_SERVER_URL)

    db = server[COUCHDB_DATABASE_NAME]

    mango_query = {
            "selector": {}
        }
    
    notes = list(db.find(mango_query))
    
    return [convert_creation_date_to_date(note) for note in notes]

    