import json

class Refrigerator:
    def __init__(self, brand, model, capacity, color, doortypes, AppCompatible, WorksWith, price):
        self.brand = brand
        self.model = model
        self.capacity = capacity
        self.color = color
        self.doortypes = doortypes
        self.WorksWith = WorksWith
        self.AppCompatible = AppCompatible
        self.price = price

# Create a Refrigerator instance using keyword arguments
refrigerator = Refrigerator(
    brand="LG",
    model="LRFLC2706S",
    capacity="26.5 cubic feet",
    color="Stainless Steel",
    doortypes=3,
    WorksWith="Amazon Alexa, Google Assistant",
    AppCompatible="Yes",
    price=1899.99
)

# Dump the Refrigerator object to JSON
json_data = json.dumps(refrigerator.__dict__, indent=4)

with open("jsonAppliance.json", "w") as json_file:
    json_file.write(json_data)

# Load JSON data from the file
with open("jsonAppliance.json", "r") as json_file:
    loaded_data = json.load(json_file)

# Create a new Refrigerator instance from loaded data
loaded_refrigerator = Refrigerator(**loaded_data)

# Print the loaded data
print("Loaded Refrigerator:")
print("Brand:", loaded_refrigerator.brand)
print("Model:", loaded_refrigerator.model)
print("Capacity:", loaded_refrigerator.capacity)
print("Color:", loaded_refrigerator.color)
print("Doortypes:", loaded_refrigerator.doortypes)
print("Works With:", loaded_refrigerator.WorksWith)
print("App Compatible:", loaded_refrigerator.AppCompatible)
print("Price:", loaded_refrigerator.price)
