
from couchdb.client import Server


server = Server("https://admin:admin@couchdb-asd6.onrender.com")

db = server["test-db"]

mango_query = {
        "selector": {}
    }

print(dict(list(db.find(mango_query))[0]))