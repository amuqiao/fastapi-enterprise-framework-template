[Linux 环境修改 uv 镜像源](https://www.notion.so/Linux-uv-215e37c651ab8007b0caeeadc73e2eea?pvs=21)

# **uv 命令行指定镜像源**

在使用`uv`安装依赖时，可以临时指定镜像源：

```powershell
uv install --index-url https://pypi.tuna.tsinghua.edu.cn/simple package-name
```

用户级别配置文件：

# **用户级别配置**

- 在`%APPDATA%\uv\uv.toml`**中配置镜像源**

```powershell
[[index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true 

```

# **项目级别配置**

- **在 pyproject.toml 中配置镜像源**
    
    如果你使用`poetry`或`setuptools`作为构建后端，可以在`pyproject.toml`中指定镜像源。
    
    ```powershell
    [[tool.uv.index]]
    url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/"
    default = true
    ```
    
- 阿里源

```python
[tool.uv]
index-url = "https://mirrors.aliyun.com/pypi/simple/"
```

- 清华源

```python
[tool.uv]
index-url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/"
```

# **验证配置是否生效**

安装依赖时观察输出，确认是否从指定镜像源下载：

```powershell
(uv_test) PS E:\test\uv_test_project\uv_test> uv pip install numpy --verbose  
DEBUG uv 0.7.2 (481d05d8d 2025-04-30)
DEBUG Searching for default Python interpreter in virtual environments
DEBUG Found `cpython-3.12.7-windows-x86_64-none` at `E:\test\uv_test_project\uv_test\.venv\Scripts\python.exe` (active virtual environment)
DEBUG Using Python 3.12.7 environment at: .venv
DEBUG Acquired lock for `.venv`
DEBUG At least one requirement is not satisfied: numpy
DEBUG Using request timeout of 30s
DEBUG Solving with installed Python version: 3.12.7
DEBUG Solving with target Python version: >=3.12.7
DEBUG Adding direct dependency: numpy*
DEBUG Acquired lock for `C:\Users\97821\AppData\Local\uv\cache\simple-v15\index\e367fd55faf540ee\numpy.lock`
DEBUG Found fresh response for: https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/numpy/
DEBUG Released lock at `C:\Users\97821\AppData\Local\uv\cache\simple-v15\index\e367fd55faf540ee\numpy.lock`
DEBUG Searching for a compatible version of numpy (*)
DEBUG Selecting: numpy==2.2.6 [compatible] (numpy-2.2.6-cp312-cp312-win_amd64.whl)
DEBUG Acquired lock for `C:\Users\97821\AppData\Local\uv\cache\wheels-v5\index\e367fd55faf540ee\numpy\numpy-2.2.6-cp312-cp312-win_amd64.lock`
DEBUG Found fresh response for: https://mirrors.tuna.tsinghua.edu.cn/pypi/web/packages/36/fa/8c9210162ca1b88529ab76b41ba02d433fd54fecaf6feb70ef9f124683f1/numpy-2.2.6-cp312-cp312-win_amd64.whl
DEBUG Released lock at `C:\Users\97821\AppData\Local\uv\cache\wheels-v5\index\e367fd55faf540ee\numpy\numpy-2.2.6-cp312-cp312-win_amd64.lock`
DEBUG Tried 1 versions: numpy 1
DEBUG marker environment resolution took 0.004s
Resolved 1 package in 4ms
DEBUG Registry requirement already cached: numpy==2.2.6
DEBUG Unnecessary package: annotated-types==0.7.0
DEBUG Unnecessary package: anyio==4.9.0
DEBUG Unnecessary package: certifi==2025.4.26
DEBUG Unnecessary package: charset-normalizer==3.4.2
DEBUG Unnecessary package: fastapi==0.115.12
DEBUG Unnecessary package: idna==3.10
DEBUG Unnecessary package: pydantic==2.11.5
DEBUG Unnecessary package: pydantic-core==2.33.2
DEBUG Unnecessary package: requests==2.32.3
DEBUG Unnecessary package: sniffio==1.3.1
DEBUG Unnecessary package: starlette==0.46
DEBUG Unnecessary package: typing-extensions==4.13.2
DEBUG Unnecessary package: typing-inspection==0.4.1
DEBUG Unnecessary package: urllib3==2.4.0
DEBUG Failed to hardlink `E:\test\uv_test_project\uv_test\.venv\Lib\site-packages\numpy\char\__init__.py` to `C:\Users\97821\AppData\Local\uv\cache\archive-v0\7zJPCsZq7N8DzcxSy5h-L\numpy\char\__init__.py`, attempting to copy files as a fallback
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 1 package in 329ms
 + numpy==2.2.6
DEBUG Released lock at `E:\test\uv_test_project\uv_test\.venv\.lock`
# 输出中应包含类似 "Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple"
```

# **常用镜像源地址**

| **镜像源** | **URL 地址** |
| --- | --- |
| 清华大学 | **https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/** |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple/ |
| 豆瓣 | https://pypi.douban.com/simple/ |
| 腾讯云 | https://mirrors.cloud.tencent.com/pypi/simple |
|  |  |

| 镜像名称 | 镜像URL | 备注 |
| --- | --- | --- |
| 清华大学镜像源 | https://pypi.tuna.tsinghua.edu.cn/simple/ | 国内最常用，更新及时，覆盖广 |
| 阿里云镜像源 | https://mirrors.aliyun.com/pypi/simple/ | 阿里云提供，稳定性较好 |
| 豆瓣镜像源 | https://pypi.doubanio.com/simple/ | 适合部分依赖较少的项目 |
| 华为云镜像源 | https://repo.huaweicloud.com/repository/pypi/simple/ | 华为云提供，企业级稳定性 |
| 腾讯云镜像源 | https://mirrors.cloud.tencent.com/pypi/simple/ | 腾讯云提供，覆盖国内多个节点 |

**提示**：若遇到镜像源不可用（如403/503错误），可尝试切换其他镜像源。建议优先选择清华或阿里云镜像源。