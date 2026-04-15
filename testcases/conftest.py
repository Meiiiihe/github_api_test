# testcases/conftest.py
import sys
import os
import pytest
import time

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 现在可以正常导入
from api.github_api import GitHubAPI

@pytest.fixture
def github_api():
    """提供GitHub API客户端实例"""
    return GitHubAPI()

@pytest.fixture
def unique_repo_name():
    """生成唯一的仓库名（避免冲突）"""
    timestamp = int(time.time())
    return f"test-repo-{timestamp}"

@pytest.fixture
def cleanup_repo(github_api):
    """测试后自动清理仓库的fixture"""
    created_repos = []
    
    def _create_and_track(repo_name):
        created_repos.append(repo_name)
        return github_api.create_repo(repo_name)
    
    yield _create_and_track
    
    # 测试结束后清理
    for repo_name in created_repos:
        try:
            github_api.delete_repo(repo_name)
            print(f"\n🧹 已清理仓库: {repo_name}")
        except:
            pass