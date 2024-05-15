from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField


class Note(Document):
    title = TextField()
    content = TextField()
    creation_date = DateTimeField(default=datetime.now)
    autor = TextField()