import os
from pymongo import MongoClient

# prod | dev | local
env, uri = os.environ.get('ENV'), os.environ.get('MONGO_URI')
client= MongoClient(uri)

print(f'===> Load {env} enviroment')
database_string = f"urlShortner_{env}"
db = client[database_string]