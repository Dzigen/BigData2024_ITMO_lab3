import os 
from ansible_vault import Vault
from pathlib import Path
from dataclasses import dataclass

SECRET_PATH = Path.joinpath(Path(__file__).parent.parent.resolve(), 'vault.yaml')

PASSWORD_PATH = Path.joinpath(Path(__file__).parent.parent.resolve(), '.vault_pass')
PASSWORD_ENV_NAME = 'MODELAPI_VAULT_PASS'

@dataclass
class Secrets:
    MONGO_MODELDB_USER_USERNAME: str = None
    MONGO_MODELDB_USER_PASSWORD: str = None
    MONGO_MODELDB_NAME: str = None
    MONGO_TABLE_NAME: str = None

    @classmethod
    def load(cls) -> None:
        try:
            vault = Vault(Path(PASSWORD_PATH).read_text())
        except FileNotFoundError:
            try:
                vault = Vault(os.environ[PASSWORD_ENV_NAME])
            except KeyError:
                raise AttributeError

        data = vault.load(open(SECRET_PATH).read())
        return cls(**data)

secrets = Secrets().load()

if __name__ == "__main__":
    print(secrets.MONGO_MODELDB_USER_USERNAME, secrets.MONGO_MODELDB_USER_PASSWORD, 
          secrets.MONGO_MODELDB_NAME, secrets.MONGO_TABLE_NAME)