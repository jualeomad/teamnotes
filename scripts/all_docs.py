
from couchdb.client import Server


server = Server("http://admin1:admin1@localhost:5984")

db = server["exampledb"]

mango_query = {
        "selector": {}
    }

print(dict(list(db.find(mango_query))[0]))

