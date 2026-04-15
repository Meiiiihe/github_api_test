# api/github_api.py
import requests
from config.config import Config

class GitHubAPI:
    """封装GitHub API的常用操作"""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.headers = Config.HEADERS
        self.username = Config.USERNAME
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_user(self, username):
        """获取用户信息"""
        response = self.session.get(f"{self.base_url}/users/{username}")
        return response
    
    def get_authenticated_user(self):
        """获取当前登录用户"""
        response = self.session.get(f"{self.base_url}/user")
        return response
    
    def create_repo(self, name, description="", private=False):
        """创建仓库"""
        data = {
            "name": name,
            "description": description,
            "private": private
        }
        response = self.session.post(f"{self.base_url}/user/repos", json=data)
        return response
    
    def delete_repo(self, repo_name):
        """删除仓库"""
        response = self.session.delete(
            f"{self.base_url}/repos/{self.username}/{repo_name}"
        )
        return response
    
    def get_repo(self, repo_name):
        """获取仓库信息"""
        response = self.session.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}"
        )
        return response