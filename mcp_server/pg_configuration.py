from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    database: str
    user: str
    password: str
    port: str = "5432"

    @classmethod
    def from_env(cls, env_dict: dict) -> 'DatabaseConfig':
        return cls(
            host=env_dict.get('PG_HOST', 'localhost'),
            database=env_dict.get('PG_DATABASE', ''),
            user=env_dict.get('PG_USER', ''),
            password=env_dict.get('PG_PASSWORD', ''),
            port=env_dict.get('PG_PORT', '5432')
        )
