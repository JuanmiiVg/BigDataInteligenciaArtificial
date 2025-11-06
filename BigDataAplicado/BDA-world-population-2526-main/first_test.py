from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo

# Replace the placeholder with your Atlas connection string
uri = ""

# Create a MongoClient with a MongoClientOptions object to set the Stable API version
client = MongoClient(uri, server_api=ServerApi(
    version='1', strict=True, deprecation_errors=True))

try:
    # Connect the client to the server (optional starting in v4.7)
    #client.connect()

    # Send a ping to confirm a successful connection
    client.admin.command({'ping': 1})
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Connection tested
    print("Choosing database: big-data-aplicado")
    database = client["big-data-aplicado"]
    print("Collection list:")
    collection_list = database.list_collections()
    for c in collection_list:
        print(c["name"])
    print("Country list:")
    population = database["datos-prueba"]

    results = population.find().sort("Population 2025", pymongo.DESCENDING)

    for d in results:
        print(f"{d['Country (or dependency)']}: {d['Population 2025']}")
finally:
    # Ensures that the client will close when you finish/error
    client.close()
