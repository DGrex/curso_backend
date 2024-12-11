from pymongo import MongoClient
# conectarse a local
#db_client = MongoClient().local

# Conectarse a remoto
db_client = MongoClient("mongodb+srv://test:test@cluster0.mwlsi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

