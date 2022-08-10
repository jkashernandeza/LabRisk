#Libraries ###################################################################################
from pymongo import MongoClient
import pymongo
##############################################################################################

def get_tweet_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://tool:oxyByZXHUZ4vPhvN@tweets.2dcuiq8.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    return client["tweetdb"]