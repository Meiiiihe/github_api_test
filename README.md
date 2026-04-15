# GitHub API 接口自动化测试框架

基于 Python + Pytest + Requests 的 GitHub REST API 自动化测试框架，覆盖用户管理、仓库操作、搜索等核心业务场景。

## 技术栈

- **语言**：Python 3.12
- **测试框架**：Pytest
- **请求库**：Requests
- **报告**：Allure / pytest-html
- **CI/CD**：GitHub Actions

## 项目结构

```
github_api_test/
├── api/
│   ├── __init__.py
│   └── github_api.py        # API封装层 + 响应封装(APIResponse)
├── config/
│   ├── __init__.py
│   └── config.py           # 配置管理(支持环境变量)
├── testcases/
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_github_api.py  # 基础API测试
│   ├── test_github_advanced.py  # 高级测试用例
│   └── test_data_driven.py # 数据驱动测试
├── data/
│   ├── __init__.py
│   └── repo_test_data.yaml  # YAML测试数据
├── utils/
│   ├── __init__.py
│   └── logger.py           # 日志工具
├── pytest.ini
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Meiiiihe/github_api_test.git
cd github_api_test
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# Linux/Mac
export GITHUB_TOKEN="your_github_token"
export GITHUB_USERNAME="your_username"

# Windows (PowerShell)
$env:GITHUB_TOKEN="your_github_token"
$env:GITHUB_USERNAME="your_username"
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest testcases/test_github_api.py

# 生成HTML报告
pytest --html=report.html --self-contained-html

# 生成Allure报告
pytest --alluredir=allure-results
allure serve allure-results
```

## 核心特性

### APIResponse 封装
```python
response = api.get_user("octocat")
if response.is_success:
    print(response.data["login"])
```

### 自动重试机制
- 429 (Rate Limit)、5xx 错误自动重试3次
- 退避策略：0.5s 递增

### 数据驱动测试
```yaml
# data/repo_test_data.yaml
create_repo_tests:
  - name: "valid-repo"
    expected_status: 201
```

## 测试用例

| 测试类 | 覆盖范围 |
|--------|----------|
| `TestGitHubUserAPI` | 用户信息、认证用户 |
| `TestGitHubRepoAPI` | 仓库CRUD、名称验证 |
| `TestGitHubSearchAPI` | 仓库搜索、排序、分页 |
| `TestDataDriven` | YAML数据驱动 |

## License

MIT
