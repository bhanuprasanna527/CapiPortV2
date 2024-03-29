from pymongo import MongoClient
import socket
from dotenv import load_dotenv
import os
import urllib
import streamlit as st

load_dotenv()


def mongodb_push_data(company_name_to_symbol, number_of_symbols):

    username = urllib.parse.quote_plus(os.environ.get("USERNAME"))
    password = urllib.parse.quote_plus(os.environ.get("PASSWORD"))
    # client = "mongodb+srv://bhanuprasanna:<password>@capiport.xtnx5it.mongodb.net/"
    MONGO_DB_URI = "mongodb+srv://%s:%s@capiport.xtnx5it.mongodb.net/" % (
        username,
        password,
    )

    st.write(MONGO_DB_URI)

    # client = MongoClient(MONGO_DB_URI)
    # if "capiport" in client.list_database_names():
    #     db = client["capiport"]
    # else:
    #     db = client["capiport"]
    # collection = db["stocks they picked"]
    # hostname = socket.gethostname()
    # ip_address = socket.gethostbyname(hostname)
    # data = {
    #     "hostname": hostname,
    #     "stocks_picked": company_name_to_symbol,
    #     "number_of_stocks_picked": number_of_symbols,
    #     "ip_address": ip_address,
    # }
    # collection.insert_one(data)
    # client.close()
