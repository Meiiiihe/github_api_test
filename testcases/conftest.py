import sys
import os
import pytest
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.github_api import GitHubAPI


@pytest.fixture
def github_api():
    api = GitHubAPI()
    yield api
    api.close()


@pytest.fixture
def unique_repo_name():
    timestamp = int(time.time() * 1000) % 1000000
    return f"test-repo-{timestamp}"


@pytest.fixture
def cleanup_repo(github_api):
    created_repos = []

    def _create_and_track(repo_name):
        created_repos.append(repo_name)
        return github_api.create_repo(repo_name)

    yield _create_and_track

    for repo_name in created_repos:
        try:
            github_api.delete_repo(repo_name)
            print(f"\n🧹 已清理仓库: {repo_name}")
        except Exception:
            pass


@pytest.fixture(scope="session", autouse=True)
def verify_token():
    from config.config import TOKEN

    if not TOKEN:
        print("\n⚠️ 警告：未设置 GITHUB_TOKEN 环境变量，部分测试可能失败")
