import mysql.connector
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

class SaveDataMySQL:
    
    def __init__ (self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.cnx = None
        self.cursor = None
    
    def connect_mysql(self):
        self.cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

    def create_cursor(self):
        self.cursor = self.cnx.cursor(buffered=True)
        return self.cursor
    
    def create_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    
    def show_databases(self):
        self.cursor.execute("SHOW DATABASES;")
        for db in self.cursor:
            print(db)
    
    def create_product_table(self, db_name, tb_name):
        self.cursor.execute(f"USE {db_name};")
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                id VARCHAR(100),
                Produto VARCHAR(100),
                Categoria_Produto VARCHAR(100),
                Preco FLOAT(10,2),
                Frete FLOAT(10,2),
                Data_Compra DATE,
                Vendedor VARCHAR(100),
                Local_Compra VARCHAR(100),
                Avaliacao_Compra INT,
                Tipo_Pagamento VARCHAR(100),
                Qntd_Parcelas INT,
                Latitude FLOAT(10,2),
                Longitude FLOAT(10,2),
                PRIMARY KEY (id)
            );
        """)
    
    def show_tables(self, db_name):
        self.cursor.execute(f"USE {db_name};")
        self.cursor.execute("SHOW TABLES;")
        for tb in self.cursor:
            print(tb)
    
    def read_csv(self, path):
        df = pd.read_csv(path)
        return df

    def add_product_data(self, df, db_name, tb_name):
        lista = [tuple(row) for _, row in df.iterrows()]
        sql = f"""
            INSERT INTO {db_name}.{tb_name}
            (id, Produto, Categoria_Produto, Preco, Frete, Data_Compra, Vendedor,
             Local_Compra, Avaliacao_Compra, Tipo_Pagamento, Qntd_Parcelas, Latitude, Longitude)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.executemany(sql, lista)
        self.cnx.commit()
        print(f"\n{self.cursor.rowcount} dados foram inseridos na tabela {tb_name}.")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()


if __name__ == "__main__":
    # Criando a instância e conectando ao MySQL
    db = SaveDataMySQL("localhost", "millenagena", "12345")
    db.connect_mysql()
    db.create_cursor()

    # Criando o banco de dados e a tabela
    db.create_database("db_produtos_teste")
    db.show_databases()
    db.create_product_table("db_produtos_teste", "tb_livros")
    db.show_tables("db_produtos_teste")

    # Lendo o CSV e inserindo os dados
    df = db.read_csv("../data_teste/tbl_livros.csv")
    db.add_product_data(df, "db_produtos_teste", "tb_livros")
    db.close()
