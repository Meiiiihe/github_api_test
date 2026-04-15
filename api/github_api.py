from __future__ import annotations
from typing import Optional, Dict, Any
from dataclasses import dataclass
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import time

import config.config as cfg


@dataclass
class APIResponse:
    status_code: int
    data: Any
    headers: Dict[str, str]
    elapsed: float

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        return 500 <= self.status_code < 600


class GitHubAPI:
    def __init__(self, username: Optional[str] = None, token: Optional[str] = None):
        self.base_url = cfg.BASE_URL
        self.username = username or cfg.USERNAME
        self._token = token or cfg.TOKEN
        self._session: Optional[requests.Session] = None

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"token {self._token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python-Pytest-Test",
        }

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(self.headers)
            adapter = HTTPAdapter(
                max_retries=Retry(
                    total=3,
                    backoff_factor=0.5,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
            )
            self._session.mount("https://", adapter)
            self._session.mount("http://", adapter)
        return self._session

    def _request(self, method: str, url: str, **kwargs) -> APIResponse:
        start_time = time.time()
        response = self.session.request(method, url, **kwargs)
        elapsed = time.time() - start_time

        try:
            data = response.json() if response.content else None
        except Exception:
            data = response.text

        return APIResponse(
            status_code=response.status_code,
            data=data,
            headers=dict(response.headers),
            elapsed=elapsed,
        )

    def get_user(self, username: str) -> APIResponse:
        return self._request("GET", f"{self.base_url}/users/{username}")

    def get_authenticated_user(self) -> APIResponse:
        return self._request("GET", f"{self.base_url}/user")

    def update_user(self, **kwargs) -> APIResponse:
        return self._request("PATCH", f"{self.base_url}/user", json=kwargs)

    def list_user_repos(
        self, username: str, sort: str = "updated", per_page: int = 30
    ) -> APIResponse:
        params = {"sort": sort, "per_page": per_page}
        return self._request(
            "GET", f"{self.base_url}/users/{username}/repos", params=params
        )

    def create_repo(
        self, name: str, description: str = "", private: bool = False, **kwargs
    ) -> APIResponse:
        data = {"name": name, "description": description, "private": private, **kwargs}
        return self._request("POST", f"{self.base_url}/user/repos", json=data)

    def get_repo(self, repo_name: str, owner: str = "") -> APIResponse:
        owner_str = owner if owner else self.username
        return self._request("GET", f"{self.base_url}/repos/{owner_str}/{repo_name}")

    def update_repo(self, repo_name: str, **kwargs) -> APIResponse:
        return self._request(
            "PATCH", f"{self.base_url}/repos/{self.username}/{repo_name}", json=kwargs
        )

    def delete_repo(self, repo_name: str, owner: str = "") -> APIResponse:
        owner_str = owner if owner else self.username
        return self._request("DELETE", f"{self.base_url}/repos/{owner_str}/{repo_name}")

    def search_repos(
        self,
        query: str,
        sort: Optional[str] = None,
        order: str = "desc",
        per_page: int = 30,
    ) -> APIResponse:
        params = {"q": query, "per_page": per_page, "order": order}
        if sort:
            params["sort"] = sort
        return self._request(
            "GET", f"{self.base_url}/search/repositories", params=params
        )

    def list_org_repos(self, org: str, per_page: int = 30) -> APIResponse:
        params = {"per_page": per_page}
        return self._request("GET", f"{self.base_url}/orgs/{org}/repos", params=params)

    def get_rate_limit(self) -> APIResponse:
        return self._request("GET", f"{self.base_url}/rate_limit")

    def close(self):
        if self._session:
            self._session.close()
            self._session = None
