uv 是一个高性能的 Python 包管理器和虚拟环境管理工具，它兼容 pip 命令并提供更快的性能。以下是使用 uv 管理 Python 项目依赖的详细指南，包括 Linux 和 Windows 环境下的不同终端使用方式。

## 1. 安装 uv

首先需要安装 uv：

- **Linux/macOS**:
    
    ```bash
    curl -LsSf <https://astral.sh/uv/install.sh> | sh
    ```
    
- **Windows PowerShell**:
    
    ```powershell
    irm <https://astral.sh/uv/install.ps1> | iex
    
    ```
    

## 2. 创建并激活虚拟环境

### 创建虚拟环境

- **指定 Python 版本**:
    
    ```bash
    # Linux/macOS
    uv venv --python=3.10
    
    # Windows PowerShell
    uv venv --python=3.10
    ```
    

### 激活虚拟环境

- **Linux/macOS (Bash/Zsh)**:
    
    ```bash
    source .venv/bin/activate
    ```
    
- **Windows PowerShell**:
    
    ```powershell
    .venv\\Scripts\\Activate.ps1
    ```
    
- **Windows Command Prompt**:
    
    ```bash
    .venv\\Scripts\\activate.bat
    ```
    

## 3. 临时指定国内镜像源

使用 `--index-url` 参数临时指定国内镜像源：

```bash
# 使用阿里云镜像源
uv pip install requests --index-url=https://mirrors.aliyun.com/pypi/simple/

# 使用腾讯云镜像源
uv pip install requests --index-url=https://mirrors.cloud.tencent.com/pypi/simple/

# 使用清华大学镜像源
uv pip install requests --index-url=https://pypi.tuna.tsinghua.edu.cn/simple/

```

## 4. 依赖包管理

### 安装依赖包

```bash
# 安装单个包
uv pip install requests

# 安装指定版本的包
uv pip install requests==2.31.0

# 安装包到开发环境
uv pip install -e .

# 从 requirements.txt 安装所有依赖
uv pip install -r requirements.txt
```

### 删除依赖包

```bash
# 删除单个包
uv pip uninstall requests

# 删除多个包
uv pip uninstall requests beautifulsoup4

```

### 更新依赖包

```bash
# 更新单个包到最新版本
uv pip install --upgrade requests

# 更新所有包
uv pip install --upgrade

# 更新指定版本范围内的包
uv pip install requests>=2.30.0,<3.0.0

```

### 查询依赖包

```bash
# 列出已安装的包
uv pip list

# 查看包的详细信息
uv pip show requests

# 检查包是否有更新
uv pip list --outdated

```

## 5. 重新安装依赖包

```bash
# 重新安装单个包
uv pip install --force-reinstall requests

# 重新安装所有依赖包
uv pip install --force-reinstall -r requirements.txt

```

## 6. 导出依赖列表

```bash
# 导出到 requirements.txt
uv pip freeze > requirements.txt

# 导出开发环境依赖
uv pip freeze --dev > requirements-dev.txt

# 导出更精确的依赖（包括依赖的依赖）
uv pip export > requirements.txt

```

## 7. 其他常用命令

```bash
# 清理缓存
uv cache clean

# 检查依赖冲突
uv pip check

# 安装预发布版本
uv pip install requests --pre

```

## 注意事项

- uv 的命令格式基本与 pip 兼容，大部分 pip 命令可以直接替换为 `uv pip` 使用
- 在 Windows PowerShell 中，执行脚本可能需要先设置执行策略：`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- 虚拟环境创建后，会在当前目录生成 `.venv` 文件夹，包含完整的 Python 环境

使用 uv 可以显著提高依赖管理的速度和效率，尤其是在大型项目中。