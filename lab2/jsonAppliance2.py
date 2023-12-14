# jsonAppliance.py

import json

# Define a Python appliance object
appliance = {
    "name": "Refrigerator",
    "brand": "Samsung",
    "model": "RF1234",
    "color": "Stainless Steel",
    "capacity": "20 cubic feet",
    "energy_rating": "A++",
}

# Write the appliance object to a JSON file
with open("jsonAppliance.json", "w") as json_file:
    json.dump(appliance, json_file)

# Read the JSON file back in as a Python object and display it
with open("jsonAppliance.json", "r") as json_file:
    loaded_appliance = json.load(json_file)
    print("Loaded Appliance:")
    print(loaded_appliance)

if __name__ == "__main__":
    pass
