from pymongo import MongoClient
import pandas as pd

uri = "mongodb+srv://delluser:harsh@cluster0.hh7ijb9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["traffic_db"]
collection = db["traffic_data"]

# Load CSV
df = pd.read_csv("traffic.csv")

# Convert to dictionary
data = df.to_dict(orient="records")

# Optional: clear old data (avoid duplicates)
collection.delete_many({})

# Insert data
collection.insert_many(data)

print("Data uploaded successfully!")