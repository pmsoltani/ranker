import json
from pathlib import Path
from typing import List

from environs import Env


env = Env()
env.read_env()

APP_ENV = env("APP_ENV", "development")


def read_json_config(path: Path) -> List[dict]:
    with open(path, "r") as urls_file:
        return json.loads(urls_file.read())


class DBConfig(object):
    DATA_DIR = env("DATA_DIR", "data")
    MAIN_DIR = Path.cwd() / DATA_DIR

    DIALECT = env("DIALECT")
    with env.prefixed(f"{DIALECT.upper()}_"):
        _DRIVER = env("DRIVER")
        _USER = env("USER")
        _PASS = env("PASS")
        _HOST = env("HOST")
        _PORT = env("PORT")
        _NAME = env("NAME")
    DB_URI = f"{DIALECT}+{_DRIVER}://{_USER}:{_PASS}@{_HOST}:{_PORT}/{_NAME}"
    GRID_DATABASE_DIR = env.list(
        "GRID_DATABASE_DIR", ["data", "grid", "full_tables"]
    )
    GRID_DATABASE_DIR = Path.cwd().joinpath(*GRID_DATABASE_DIR)

    RANKINGS: dict
    _rankings_file_path = env.path("RANKINGS_FILE_PATH", "rankings.json")
    with open(_rankings_file_path, "r") as json_file:
        RANKINGS = json.loads(json_file.read())

    MATCHES: dict = {}
    _matches_file_path = env.path("MATCHES_FILE_PATH", "matches.json")
    if _matches_file_path:
        with open(_matches_file_path, "r") as json_file:
            MATCHES = json.loads(json_file.read())


class CrawlerConfig(object):
    DATA_DIR = env("DATA_DIR", "data")
    MAIN_DIR = Path.cwd() / DATA_DIR

    USER_AGENT = env("USER_AGENT")

    CRAWLER_ENGINE = env.list("CRAWLER_ENGINE", ["qs", "shanghai", "the"])
    _country_names_path = env("COUNTRY_NAMES", "country_names.json")
    COUNTRY_NAMES = read_json_config(_country_names_path)


class QSConfig(CrawlerConfig):
    headers = {"User-Agent": CrawlerConfig.USER_AGENT}
    BASE_URL = env("QS_BASE")
    _raw_urls = env("QS_URLS_FILE", "qs_urls.json")
    URLS = read_json_config(Path.cwd() / _raw_urls)

    DOWNLOAD_DIR = CrawlerConfig.MAIN_DIR / "qs"

    FIELDS = {
        "RANK": "Rank",
        "# RANK": "Rank",
        "UNIVERSITY": "Institution",
        "URL": "URL",
        "LOCATION": "Country",
        "OVERALL SCORE": "Overall Score",
        "Academic Reputation": "Academic Reputation",
        "Employer Reputation": "Employer Reputation",
        "Faculty Student": "Faculty Student",
        "International Faculty": "International Faculty",
        "International Students": "International Students",
        "Citations per Faculty": "Citations per Faculty",
    }


class ShanghaiConfig(CrawlerConfig):
    headers = {"User-Agent": CrawlerConfig.USER_AGENT}
    BASE_URL = env("SHANGHAI_BASE")
    _raw_urls = env("SHANGHAI_URLS_FILE", "shanghai_urls.json")
    URLS = read_json_config(Path.cwd() / _raw_urls)

    DOWNLOAD_DIR = CrawlerConfig.MAIN_DIR / "shanghai"

    FIELDS = {
        "World Rank": "Rank",
        "URL": "URL",
        "National/RegionalRank": "National Rank",
        "National/Regional Rank": "National Rank",
        "Total Score": "Total Score",
    }


class THEConfig(CrawlerConfig):
    headers = {"User-Agent": CrawlerConfig.USER_AGENT}
    BASE_URL = env("THE_BASE")
    _raw_urls = env("THE_URLS_FILE", "the_urls.json")
    URLS = read_json_config(Path.cwd() / _raw_urls)

    DOWNLOAD_DIR = CrawlerConfig.MAIN_DIR / "the"

    FIELDS = {
        "Rank": "Rank",
        "URL": "URL",
        "Overall": "Overall",
        "Teaching": "Teaching",
        "Research": "Research",
        "Citations": "Citations",
        "Industry Income": "Industry Income",
        "International Outlook": "International Outlook",
        "No. of FTE Students": "No. of FTE Students",
        "No. of students per staff": "No. of students per staff",
        "International Students": "International Students",
        "Female:Male Ratio": "Female:Male Ratio",
        "Overall": "Overall",
        "Teaching": "Teaching",
        "Research": "Research",
        "Citations": "Citations",
        "Industry Income": "Industry Income",
        "International Outlook": "International Outlook",
    }
