import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DatabaseConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            uri = st.secrets['URI_STR']
            cls._instance.client = MongoClient(uri, server_api = ServerApi('1'))
        return cls._instance
