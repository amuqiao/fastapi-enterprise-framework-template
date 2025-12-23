# **1. 核心作用**

- **锁定版本**：记录所有依赖（直接+传递性）的确切版本号和哈希值，确保环境一致性。
- **消除差异**：避免因依赖版本浮动（如 `requests>=2.32.0` 可能安装不同小版本）导致的 Bug。

# **2. 正确使用方式**

| 场景 | 命令示例 | 说明 |
| --- | --- | --- |
| **初始化项目** | `uv sync` | 根据 `uv.lock` 安装依赖（若无则生成）。 |
| **升级依赖** | `uv update --all` | 更新所有依赖并生成新的 `uv.lock`。 |
| **添加新依赖** | `uv add package-name` | 修改 `pyproject.toml` 并更新 `uv.lock`。 |
| **部署生产环境** | `uv sync` | 严格按照 `uv.lock` 安装，确保与开发环境一致。 |
| **测试新依赖** | `uv sync --no-lock` | 忽略 `uv.lock`，按 `pyproject.toml` 最新范围安装（慎用）。 |
| **手动刷新锁文件** | `uv lock` | 重新生成 `uv.lock`（不安装依赖）。可以将`pyproject.toml`修改为指定版本后更新 |

# **3. 生命周期管理**

1. **创建**：
    - 首次执行 `uv sync` 或 `uv lock` 时自动生成。
    - 基于 `pyproject.toml` 中的依赖范围计算确切版本。
2. **更新**：
    - 通过 `uv update` 或 `uv add/remove` 命令自动更新。
    - **禁止手动编辑**，必须通过 `uv` 命令修改。
3. **版本控制**：
    - **提交到 Git**：确保团队/CI 环境使用相同依赖。
    - **同步变更**：当 `uv.lock` 更新时，团队成员需重新执行 `uv sync`。
4. **生产部署**：
    - 仅通过 `uv sync` 安装依赖，禁用 `-no-lock`。
    - 使用 `uv export --format=requirements` 生成生产依赖清单。

# **4. 关键最佳实践**

1. **提交双文件**：同时提交 `pyproject.toml`（定义范围）和 `uv.lock`（锁定版本）。
2. **更新流程**：
    
    ```bash
    # 1. 修改 pyproject.toml 中的依赖范围
    # 2. 执行更新并生成新的 uv.lock
    uv update --all
    # 3. 提交两个文件的变更
    git commit -m "Update dependencies" pyproject.toml uv.lock
    
    ```
    
3. **安全审计**：定期检查 `uv.lock` 中的依赖是否存在漏洞：
    
    ```bash
    pip-audit -r <(uv export --format=requirements)
    
    ```
    

# **5. 常见问题**

| 问题 | 解答 |
| --- | --- |
| **为什么需要 `uv.lock`？** | `pyproject.toml` 定义宽松范围（如 `>=2.32.0`），而 `uv.lock` 固定为具体版本（如 `2.32.3`）。 |
| **何时需要重新生成 `uv.lock`？** | - 修改 `pyproject.toml` 后<br>- 需要更新依赖到最新兼容版本时。 |
| **如何查看依赖树？** | `uv graph` 命令可视化依赖关系。 |
| **生产环境能否跳过 `uv.lock`？** | 禁止！跳过会导致环境不一致，推荐始终使用 `uv sync`。 |

# 其他

uv lock 依赖cpython

```bash
(.venv) ➜  servo_ai_api git:(main) ✗ uv lock
cpython-3.12.0-macos-x86_64-none (download) ------------------------------ 5.62 MiB/16.20 MiB  
```

# **总结**

`uv.lock` 是保证跨环境依赖一致性的核心工具，通过以下步骤实现高效管理：

1. **提交 `uv.lock` 到版本控制**
2. **通过 `uv` 命令自动化更新**
3. **生产环境强制校验锁文件**

这种工作流能显著减少因依赖差异导致的部署问题，是现代 Python 项目的必备实践。