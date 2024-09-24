"""Script for loading data from an external API into MongoDB."""
import requests
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


client: MongoClient = MongoClient("mongodb://root:example@localhost:27017")
db: Database = client["mydatabase"]
users_collection: Collection = db["users"]
posts_collection: Collection = db["posts"]
comments_collection: Collection = db["comments"]


def fetch_data_from_api(endpoint: str) -> list[dict] | None:
    """Fetch data from the JSONPlaceholder API.

    Args:
        endpoint (str): the endpoint to fetch data from

    Returns:
        list[dict] | None: return the data if the request is successful, otherwise return None
    """

    url = f"https://jsonplaceholder.typicode.com/{endpoint}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def store_data_in_mongodb(collection: Collection, data: list[dict]) -> None:
    """Store data in MongoDB.

    Args:
        collection (Collection): the MongoDB collection to store the data in
        data (list[dict]): the data to store in the MongoDB collection
    """
    if data:
        collection.insert_many(data)
        print(f"Inserted {len(data)} documents into the {collection.name} collection.")
    else:
        print(f"No data to store in the {collection.name} collection.")


if __name__ == "__main__":

    endpoints = ["users", "posts", "comments"]

    for endpoint in endpoints:
        print(f"Fetching {endpoint} from JSONPlaceholder API...")
        data = fetch_data_from_api(endpoint)
        if data:
            print(f"Storing {endpoint} in MongoDB...")
            store_data_in_mongodb(db[endpoint], data)
    print("Data fetching and storage complete.")
