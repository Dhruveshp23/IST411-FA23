# Project: Lab 4 MongoDB
# Purpose Details: Learn how to use Python3 to download a JSON payload and save it into MongoDB
# Course: IST 411
# Author: Dhruvesh Patel
# Date Developed: 9/12/23
# Last Date Changed: 9/13/23

# Import necessary libraries
import requests
from pymongo import MongoClient

# Define the URL for the JSON payload
json_url = "https://jsonplaceholder.typicode.com/posts/1/comments"

# Function to fetch JSON data from the URL
def fetch_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch JSON data.")
        return None

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Assuming MongoDB is running on the default port

# Specify your database and collection names
db = client.team4 
collection = db.jsonPayloadPatelD

# Fetch JSON data
json_data = fetch_json_data(json_url)

if json_data:
    # Insert the JSON data into the MongoDB collection
    collection.insert_many(json_data)
    print("JSON data inserted into MongoDB successfully.")
else:
    print("No JSON data to insert.")


