import pytest
import time
from api.github_api import GitHubAPI
import os
from config.config import Config, TOKEN


class TestGitHubUserAdvanced:
    """用户相关高级测试"""

    def setup_method(self):
        if not TOKEN:
            print("⚠️ 警告：未设置 GITHUB_TOKEN 环境变量")
        self.api = GitHubAPI()

    def teardown_method(self):
        self.api.close()

    def test_get_user_octocat(self):
        """测试获取octocat用户"""
        r = self.api.get_user("octocat")
        assert r.status_code == 200
        assert r.data["login"] == "octocat"

    def test_get_user_google(self):
        """测试获取google用户"""
        r = self.api.get_user("google")
        assert r.status_code == 200
        assert r.data["login"] == "google"

    def test_get_user_microsoft(self):
        """测试获取microsoft用户"""
        r = self.api.get_user("microsoft")
        assert r.status_code == 200
        assert r.data["login"] == "microsoft"

    def test_get_user_apple(self):
        """测试获取apple用户"""
        r = self.api.get_user("apple")
        assert r.status_code == 200

    def test_get_user_facebook(self):
        """测试获取facebook用户"""
        r = self.api.get_user("facebook")
        assert r.status_code == 200

    def test_get_user_netflix(self):
        """测试获取netflix用户"""
        r = self.api.get_user("netflix")
        assert r.status_code == 200

    def test_get_user_spotify(self):
        """测试获取spotify用户"""
        r = self.api.get_user("spotify")
        assert r.status_code == 200

    def test_get_user_amazon(self):
        """测试获取amazon用户"""
        r = self.api.get_user("amazon")
        assert r.status_code == 200

    def test_get_user_twitter(self):
        """测试获取twitter用户"""
        r = self.api.get_user("twitter")
        assert r.status_code == 200

    def test_get_user_nonexistent(self):
        """测试获取不存在的用户 - 异常场景"""
        r = self.api.get_user("thisuserdoesnotexist12345")
        assert r.status_code == 404

    def test_user_has_email_field(self):
        """验证用户信息包含email字段"""
        r = self.api.get_user("octocat")
        assert "email" in r.data

    def test_user_has_bio_field(self):
        """验证用户信息包含bio字段"""
        r = self.api.get_user("octocat")
        assert "bio" in r.data

    def test_user_has_company_field(self):
        """验证用户信息包含company字段"""
        r = self.api.get_user("octocat")
        assert "company" in r.data

    def test_user_has_location_field(self):
        """验证用户信息包含location字段"""
        r = self.api.get_user("octocat")
        assert "location" in r.data

    def test_user_has_public_repos_field(self):
        """验证用户信息包含public_repos字段"""
        r = self.api.get_user("octocat")
        assert "public_repos" in r.data


class TestGitHubRepoAdvanced:
    """仓库相关高级测试"""

    def setup_method(self):
        self.api = GitHubAPI()

    def teardown_method(self):
        self.api.close()

    @pytest.mark.parametrize(
        "repo_name",
        [
            "test-repo-1",
            "test-repo-2",
            "test-repo-3",
            "my-test-repo",
            "demo-repo",
            "sample-repo",
            "api-test-repo",
            "pytest-demo",
            "github-api-test",
            "automation-repo",
        ],
    )
    def test_create_multiple_repos(self, repo_name):
        """批量创建仓库测试"""
        unique_name = f"{repo_name}-{int(time.time())}"
        r = self.api.create_repo(unique_name)
        assert r.status_code == 201
        self.api.delete_repo(unique_name)
        print(f"✅ 创建并删除: {unique_name}")

    @pytest.mark.parametrize(
        "name,should_fail",
        [
            ("valid-name", False),
            ("valid-name-with-numbers-123", False),
            ("valid-name-with-dashes", False),
            ("", True),
            ("a" * 101, True),
            ("test@#$", True),
            (" test", True),
            ("test ", True),
            ("TEST", False),
            ("Test-Repo-123", False),
        ],
    )
    def test_repo_name_validation(self, name, should_fail):
        """仓库名称验证测试"""
        unique_name = f"{name}-{int(time.time())}" if not should_fail else name
        r = self.api.create_repo(unique_name)

        if should_fail:
            assert r.status_code == 422
        else:
            assert r.status_code == 201
            self.api.delete_repo(unique_name)

    @pytest.mark.parametrize(
        "description",
        [
            "This is a test repository",
            "Short desc",
            "A" * 100,
            "",
            "中文描述测试",
        ],
    )
    def test_repo_description(self, description):
        """测试不同描述的仓库创建"""
        repo_name = f"desc-test-{int(time.time())}"
        r = self.api.create_repo(repo_name, description)
        assert r.status_code == 201

        repo_info = self.api.get_repo(repo_name)
        assert repo_info.data["description"] == description

        self.api.delete_repo(repo_name)
        print(f"✅ 描述测试通过: {description[:20]}")


class TestGitHubSearchAPI:
    """搜索相关API测试"""

    def setup_method(self):
        self.api = GitHubAPI()

    def teardown_method(self):
        self.api.close()

    @pytest.mark.parametrize(
        "query",
        [
            "pytest",
            "selenium",
            "requests",
            "django",
            "flask",
            "fastapi",
            "tensorflow",
            "react",
        ],
    )
    def test_search_repositories(self, query):
        """搜索仓库测试"""
        response = self.api.search_repos(query)
        assert response.status_code == 200
        data = response.data
        assert data["total_count"] > 0
        print(f"✅ 搜索 '{query}' 找到 {data['total_count']} 个仓库")

    def test_search_with_limit(self):
        """测试搜索限制结果数量"""
        response = self.api.search_repos("python", per_page=5)
        assert response.status_code == 200
        assert len(response.data["items"]) <= 5

    def test_search_with_sort(self):
        """测试搜索结果排序"""
        response = self.api.search_repos("pytest", sort="stars", order="desc")
        assert response.status_code == 200
        items = response.data["items"]
        if len(items) > 1:
            assert items[0]["stargazers_count"] >= items[1]["stargazers_count"]

    def test_search_no_results(self):
        """测试搜索无结果"""
        response = self.api.search_repos("thisquerywillnotmatchanything12345")
        assert response.status_code == 200
        assert response.data["total_count"] == 0


class TestGitHubRateLimit:
    """速率限制测试"""

    def setup_method(self):
        self.api = GitHubAPI()

    def teardown_method(self):
        self.api.close()

    def test_rate_limit_info(self):
        """测试获取速率限制信息"""
        response = self.api.get_rate_limit()
        assert response.status_code == 200
        data = response.data
        assert "resources" in data
        assert "core" in data["resources"]
        print(f"✅ API剩余调用次数: {data['resources']['core']['remaining']}")
