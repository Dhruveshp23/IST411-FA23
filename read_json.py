import json

# Replace 'YourLastName' with your actual last name
filename = 'payloadPatelD.json'

try:
    with open(filename, 'r') as file:
        payload = json.load(file)
        print("JSON Payload:")
        print(json.dumps(payload, indent=2))
except Exception as e:
    print(f"Error reading JSON file: {e}")
