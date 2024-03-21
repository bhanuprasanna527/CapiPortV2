## importing socket module
import socket
from pymongo.mongo_client import MongoClient
import urllib
import sys
import os
from dotenv import load_dotenv
load_dotenv()
import argparse

# Initialize ArgumentParser
parser = argparse.ArgumentParser(description="SECRETS")

# Add arguments
parser.add_argument('USERNAME', type=str)
parser.add_argument('PASS', type=int)

# Parse arguments
args = parser.parse_args()

# Access parsed arguments
arg1_value = args.USERNAME
arg2_value = args.PASS

# Create a new client and connect to the server
client = MongoClient("mongodb+srv://%s:%s@sankhyikii-capiport.detrwoc.mongodb.net/"%(arg1_value,arg2_value))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def MongoCon(company_name_to_symbol, number_of_symbols)->None:
    # create a new database named- "capiport"
    # if db exists, do not make, else make
    if "capiport" in client.list_database_names():
        print("Database already exists!")
        db = client["capiport"]
    else:
        db = client["capiport"]
        # print("Database created successfully!")

    # create a new collection named- "stocks they picked"
    collection = db["stocks they picked"]
    # show all the databases
    # print(client.list_database_names())
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    # save hostname, stocks_picked and ip_address in the database
    data = {
        "hostname": hostname,
        "stocks_picked": company_name_to_symbol,
        'number_of_stocks_picked': number_of_symbols,
        "ip_address": ip_address
    }
    collection.insert_one(data)
    # push these changes to the database and close the connection 
    client.close()
    print("Data inserted successfully!")
