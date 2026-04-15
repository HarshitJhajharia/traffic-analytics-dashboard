from pymongo import MongoClient

uri = "mongodb+srv://delluser:harsh@cluster0.hh7ijb9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)