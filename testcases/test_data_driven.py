# testcases/test_data_driven.py
import pytest
import yaml
import time
from api.github_api import GitHubAPI

# 加载 YAML 测试数据
with open("data/repo_test_data.yaml", "r", encoding="utf-8") as f:
    test_data = yaml.safe_load(f)

class TestDataDriven:
    """数据驱动测试 - 测试数据与脚本分离"""
    
    @pytest.mark.parametrize("case", test_data["create_repo_tests"])
    def test_create_repo_data_driven(self, case):
        """使用 YAML 数据驱动测试创建仓库"""
        api = GitHubAPI()
        
        # 对于有效名称，加上时间戳避免冲突
        if case["expected_status"] == 201:
            repo_name = f"{case['name']}_{int(time.time())}"
        else:
            repo_name = case["name"]
        
        response = api.create_repo(repo_name, case["description"], case["private"])
        
        assert response.status_code == case["expected_status"]
        
        # 清理
        if case["expected_status"] == 201:
            api.delete_repo(repo_name)
            print(f"✅ 数据驱动测试通过: {repo_name}")
        else:
            print(f"✅ 异常场景验证通过: {case['description']}")
    
    @pytest.mark.parametrize("search_case", test_data["search_tests"])
    def test_search_data_driven(self, search_case):
        """使用 YAML 数据驱动测试搜索"""
        api = GitHubAPI()
        response = api.session.get(
            f"{api.base_url}/search/repositories",
            params={"q": search_case["query"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] >= search_case["expected_min_count"]
        
        print(f"✅ 搜索 '{search_case['query']}' 找到 {data['total_count']} 个仓库")