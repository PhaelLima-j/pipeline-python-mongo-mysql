
# 📦 Projeto de Extração, Transformação e Armazenamento de Dados (MongoDB + MySQL)

Este projeto tem como objetivo extrair dados de uma API pública, transformá-los e armazená-los em dois bancos de dados distintos: **MongoDB** e **MySQL**. Além disso, os dados processados são exportados em formato `.csv`.

## 🗂 Estrutura do Projeto

```
├── data_processed/              # Arquivos de dados finais
│   └── tabela_livros.csv
├── notebooks/                   # Jupyter Notebooks para testes e exploração
│   ├── extract_and_save_data.ipynb
│   ├── save_data_mysql.ipynb
│   └── transform_data.ipynb
├── scripts/                     # Scripts Python
│   ├── extract_and_save_data.py
│   └── mongodb_class.py
├── venv/                        # Ambiente virtual
├── .env                         # Variáveis de ambiente (ex: URI do MongoDB e MySQL)
├── requirements.txt             # Bibliotecas necessárias
```

## ⚙️ Funcionalidades

- Extração de dados da API [labdados.com/produtos](https://labdados.com/produtos)
- Armazenamento inicial dos dados no **MongoDB**
- Processamento e transformação dos dados
- Armazenamento final em um banco **MySQL**
- Exportação dos dados em formato `.csv` para uso externo

## 🚀 Como Executar

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie o arquivo `.env`** com as suas credenciais:
   ```env
   MONGODB_URI=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=sua_senha
   MYSQL_DATABASE=nome_do_banco
   ```

3. **Instale as dependências**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute os scripts ou notebooks conforme necessário**  
   - Para extrair e salvar dados no MongoDB:  
     `python scripts/extract_and_save_data.py`  
   - Para transformar e salvar dados no MySQL:  
     Acesse e execute o notebook `save_data_mysql.ipynb`

## 🛠 Tecnologias Utilizadas

- Python
- MongoDB + PyMongo
- MySQL + SQLAlchemy
- Pandas
- Requests
- dotenv
