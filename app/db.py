from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


client: MongoClient = MongoClient("mongodb://root:example@localhost:27017")
db: Database = client["mydatabase"]
posts_collection: Collection = db["posts"]
comments_collection: Collection = db["comments"]
users_collection: Collection = db["users"]
