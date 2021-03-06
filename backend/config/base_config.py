import enum
from pathlib import Path
from typing import Callable, Union
from utils.get_json import get_json

from pydantic import BaseSettings, Field, validator


class DialectEnum(str, enum.Enum):
    mysql = "mysql"
    postgresql = "postgresql"


class BaseConfig(BaseSettings):
    ROOT_DIR: Path = Path.cwd()
    DATA_DIR: Path = ROOT_DIR / "data"
    RESPONSES_DIR: Path = DATA_DIR / "responses"
    MAIN_DIR: Path = ROOT_DIR / "essentials"

    COUNTRIES_FILE: Path = MAIN_DIR / "countries.csv"

    COUNTRY_NAMES_FILE: Path = MAIN_DIR / "country_names.json"
    ENTITIES_FILE: Path = MAIN_DIR / "entities.json"
    MATCHES_FILE: Path = MAIN_DIR / "matches.json"
    RANKINGS_FILE: Path = MAIN_DIR / "rankings.json"

    QS_URLS_FILE: Path = MAIN_DIR / "qs_urls.json"
    SHANGHAI_URLS_FILE: Path = MAIN_DIR / "shanghai_urls.json"
    THE_URLS_FILE: Path = MAIN_DIR / "the_urls.json"

    GRID_DATABASE_DIR: Path = DATA_DIR / "grid" / "full_tables"

    DIALECT: DialectEnum = Field(..., env="DIALECT")

    COUNTRY_NAMES: dict = {}

    @validator("COUNTRY_NAMES")
    def _load_country_names(cls, country_names, values):
        return cls.read_json(values["COUNTRY_NAMES_FILE"])

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def read_json(
        cls, file_path: Union[Path, str], object_hook: Callable = None
    ):
        return get_json(file_path=file_path, object_hook=object_hook)

    def country_name_mapper(self, country: str) -> str:
        try:
            return self.COUNTRY_NAMES.get(
                country.strip().replace("-", " ").lower(), country
            )
        except AttributeError:  # country is None
            return country
