from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField

class Note(Document):
    title = TextField()
    content = TextField()
    creation_date = DateTimeField(default=datetime.now)
    author = TextField()