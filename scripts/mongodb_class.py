from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

class MongoDBHandler:

    def __init__(self, uri, db_name, col_name):
        self.uri = uri
        self.client = None
        self.db_name = db_name
        self.col_name = col_name
        self.collection = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        try:
            self.client.admin.command('ping')
            print('✅ Conectado ao MongoDB!')
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def create_connect_db(self):
        self.db = self.client[self.db_name]
    
    def create_connect_collection(self):
        self.collection = self.db[self.col_name]

    def setup_database(self):
        self.create_connect_db()
        self.create_connect_collection()

    def extract_api_data(self, url):
        return requests.get(url).json()
    
    def insert_data(self, data):
        result = self.collection.insert_many(data)
        return len(result.inserted_ids)

    def close(self):
        if self.client:
            self.client.close()
            print("🔒 Conexão com MongoDB encerrada.")

# Script principal
if __name__ == "__main__":
    handler = MongoDBHandler(
        uri= MONGODB_URI,
        db_name="db_produtos_desafio",
        col_name="produtos"
    )

    handler.connect()
    handler.setup_database()

    data = handler.extract_api_data("https://labdados.com/produtos")
    print(f"\n📦 Quantidade de dados extraídos: {len(data)}")

    n_docs = handler.insert_data(data)
    print(f"\n✅ Documentos inseridos na coleção: {n_docs}")

    handler.close()
