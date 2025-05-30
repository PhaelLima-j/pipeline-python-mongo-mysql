from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests
import pandas as pd
import os
from dotenv import load_dotenv
MONGODB_URI = os.getenv("MONGODB_URI")

class TransformData:

    def __init__ (self, uri, db_name, col_name):
        self.uri = uri
        self.client = None
        self.db_name = db_name
        self.col_name = col_name
        self.collection = None
        self.db = None

    def connect(self):
        self.client = MongoClient (self.uri, server_api=ServerApi('1'))
        try:
            self.client.admin.command('ping')
            print('Conectado ao MongoDB!')
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def create_connect_db (self):
        self.db = self.client[self.db_name]
    
    def create_connect_collection (self):
        self.collection = self.db[self.col_name]

    def visualize_collection (self):
        for doc in self.collection.find():
            print(doc)
    
    def rename_column (self, col_name, new_name):
        self.collection.update_many({}, {"$rename": {col_name: new_name}})
        return self.collection.find_one()
    
    def select_category (self, category):
        cursor = self.collection.find({"Categoria do Produto": f"{category}"})
        lista_specific_category = []
        for doc in cursor:
            lista_specific_category.append(doc)
        return lista_specific_category
    
    def make_regex (self, regex):
        query = {"Data da Compra": {"$regex": f"{regex}"}}

        lista_regex = []
        for doc in self.collection.find(query):
            lista_regex.append(doc)

        return lista_regex

    def create_dataframe (self, lista):
        df = pd.DataFrame(lista)
        return df

    def format_date(self, df):
        df["Data da Compra"] = pd.to_datetime(df["Data da Compra"], format="%d/%m/%Y")
        df["Data da Compra"] = df["Data da Compra"].dt.strftime("%Y-%m-%d")

    def save_csv(self, df, path):
        df.to_csv(path, index=False)
   
if __name__ == "__main__":
    # Defina sua URI correta aqui
    uri = MONGODB_URI
    db_name = "db_produtos_desafio"
    col_name = "produtos"

    # Criação do objeto e conexão com MongoDB
    transformador = TransformData(uri, db_name, col_name)
    transformador.connect()
    transformador.create_connect_db()
    transformador.create_connect_collection()

    # Renomeando colunas
    transformador.rename_column("lat", "Latitude")
    transformador.rename_column("lon", "Longitude")

    # Salvando dados da categoria livros
    livros = transformador.select_category("livros")
    df_livros = transformador.create_dataframe(livros)
    transformador.format_date(df_livros)
    transformador.save_csv(df_livros, "../data_teste/tb_livros.csv")

    # Salvando produtos vendidos a partir de 2021
    produtos = transformador.make_regex("/202[1-9]")
    df_produtos = transformador.create_dataframe(produtos)
    transformador.format_date(df_produtos)
    transformador.save_csv(df_produtos, "../data_teste/tb_produtos.csv")
