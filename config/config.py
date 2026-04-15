# config/config.py
import os

class Config:
    # 从环境变量读取Token（更安全）
    TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    # GitHub API配置
    BASE_URL = "https://api.github.com"
    HEADERS = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-Pytest-Test"
    }
    
    # 你的GitHub用户名
    USERNAME = "Meiiiihe"