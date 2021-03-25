import os
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLConfig:
    user = os.getenv('POSTGRES_USER', 'admin')
    password = os.getenv('POSTGRES_PASSWORD', 'pgpassword')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    name = os.getenv('POSTGRES_DB', 'TAdAn')