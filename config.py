from database.config import PostgreSQLConfig


class AppConfig:
    Database: PostgreSQLConfig

    Database = PostgreSQLConfig()