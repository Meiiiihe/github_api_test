# testcases/test_github_api.py
import pytest
import time
from api.github_api import GitHubAPI

class TestGitHubUserAPI:
    """GitHub用户相关API测试"""
    
    def test_get_public_user(self, github_api):
        """测试获取公开用户信息"""
        response = github_api.get_user("octocat")
        
        assert response.status_code == 200
        data = response.json()
        assert data["login"] == "octocat"
        assert "id" in data
        assert "name" in data
        
        print(f"\n✅ 获取用户信息成功: {data['login']}")
    
    def test_get_authenticated_user(self, github_api):
        """测试获取当前登录用户"""
        response = github_api.get_authenticated_user()
        
        assert response.status_code == 200
        data = response.json()
        assert data["login"] == github_api.username
        
        print(f"\n✅ 当前登录用户: {data['login']}")

class TestGitHubRepoAPI:
    """GitHub仓库相关API测试"""
    
    def test_create_repo(self, github_api, unique_repo_name):
        """测试创建仓库"""
        response = github_api.create_repo(
            unique_repo_name, 
            "Created by pytest automation"
        )
        
        # 创建成功应该返回201
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == unique_repo_name
        assert data["private"] == False
        
        print(f"\n✅ 仓库创建成功: {unique_repo_name}")
        
        # 清理：删除创建的仓库
        github_api.delete_repo(unique_repo_name)
        print(f"🧹 已清理仓库: {unique_repo_name}")
    
    def test_get_repo(self, github_api, unique_repo_name):
        """测试获取仓库信息"""
        # 先创建一个仓库
        github_api.create_repo(unique_repo_name)
        
        # 等待1秒，让GitHub API同步
        time.sleep(1)
        
        # 获取仓库信息
        response = github_api.get_repo(unique_repo_name)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == unique_repo_name
        assert "owner" in data
        
        print(f"\n✅ 获取仓库信息成功: {data['full_name']}")
        
        # 清理
        github_api.delete_repo(unique_repo_name)
    
    @pytest.mark.parametrize("repo_name_prefix,expected_status", [
        ("valid-repo-name", 201),      # 有效名称
        ("", 422),                      # 空名称
        ("a" * 101, 422),              # 超长名称（超过100字符）
        ("test@#$", 422),              # 特殊字符
    ])
    def test_create_repo_with_different_names(self, github_api, repo_name_prefix, expected_status):
        """参数化测试：用不同名称创建仓库（使用时间戳确保唯一性）"""
        
        # 如果是有效名称，加上时间戳确保唯一
        if expected_status == 201:
            timestamp = int(time.time())
            repo_name = f"{repo_name_prefix}_{timestamp}"
        else:
            repo_name = repo_name_prefix
        
        response = github_api.create_repo(repo_name)
        assert response.status_code == expected_status
        
        # 如果创建成功，删除它
        if expected_status == 201:
            github_api.delete_repo(repo_name)
            print(f"\n✅ 创建并删除成功: {repo_name}")
        else:
            # 只显示前50个字符，避免输出太长
            display_name = repo_name[:50] + "..." if len(repo_name) > 50 else repo_name
            print(f"\n✅ 正确返回错误状态码 {expected_status}: {display_name}")