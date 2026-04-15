import os

TOKEN = os.getenv("GITHUB_TOKEN", "")
USERNAME = os.getenv("GITHUB_USERNAME", "Meiiiihe")
BASE_URL = "https://api.github.com"
USER_AGENT = "Python-Pytest-Test"


def get_headers() -> dict:
    return {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": USER_AGENT,
    }


class Config:
    TOKEN = TOKEN
    USERNAME = USERNAME
    BASE_URL = BASE_URL
    USER_AGENT = USER_AGENT

    @classmethod
    def get_headers(cls) -> dict:
        return {
            "Authorization": f"token {cls.TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": cls.USER_AGENT,
        }
