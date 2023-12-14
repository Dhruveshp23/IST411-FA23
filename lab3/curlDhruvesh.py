# Project: Solo Lab Python3 and CURL urllib
# Purpose Details: Use CURL tool to extract payload from internet
# Course: IST 411
# Author: Dhruvesh Patel
# Date Developed: 9/6/2023
# Last Date Changed:
# Rev: 1

# Import libraries

import urllib.request
import json

# Define the URL to fetch JSON data from
url = "https://jsonplaceholder.typicode.com/posts/1/comments"

# Fetch data from the URL
response = urllib.request.urlopen(url)
payload = response.read()

# Decode the payload into JSON format
payloadJSON = json.loads(payload.decode('utf-8'))

# Write the JSON payload to a file named curl.json
with open("curl.json", "w") as json_file:
    json.dump(payloadJSON, json_file, indent=4)

# Read the file curl.json and display the JSON payload
with open("curl.json", "r") as json_file:
    loaded_json = json.load(json_file)
    print(json.dumps(loaded_json, indent=4))


