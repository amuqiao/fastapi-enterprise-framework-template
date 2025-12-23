在 Linux 环境下配置 `uv` 工具的镜像源为国内镜像（如阿里云、清华等），可以通过环境变量或配置文件实现。以下是具体步骤：

### **方法一：通过环境变量临时配置（推荐）**

在执行 `uv venv` 命令时，直接指定 `UV_PIP_INDEX_URL` 环境变量：

```bash
UV_PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \\
UV_PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn \\
uv venv .venv --python=3.8

```

**参数说明**：

- `UV_PIP_INDEX_URL`：指定 PyPI 镜像源地址（这里使用清华镜像）。
- `UV_PIP_TRUSTED_HOST`：信任的镜像源主机（避免 SSL 验证问题）。

### **方法二：全局配置镜像源**

创建或编辑 `~/.config/uv/uv.toml` 配置文件（如果目录不存在，需手动创建）：

```bash
mkdir -p ~/.config/uv
vi ~/.config/uv/uv.toml

```

在文件中添加以下内容：

```toml
[pip]
index-url = "<https://pypi.tuna.tsinghua.edu.cn/simple>"
trusted-host = ["pypi.tuna.tsinghua.edu.cn"]

```

保存后，所有 `uv venv` 命令都会自动使用该镜像源。

### **常用国内镜像源地址**

- **清华大学**：`https://pypi.tuna.tsinghua.edu.cn/simple`
- **阿里云**：`https://mirrors.aliyun.com/pypi/simple/`
- **中国科技大学**：`https://pypi.mirrors.ustc.edu.cn/simple/`

### **验证配置是否生效**

创建虚拟环境后，查看 `pip` 配置：

```bash
source .venv/bin/activate  # 激活虚拟环境
pip config list             # 查看当前配置
```

如果输出包含镜像源地址（如 `global.index-url`），则配置成功。

### **注意事项**

1. **临时覆盖全局配置**：若同时设置了环境变量和配置文件，**环境变量优先级更高**。
2. **SSL 验证问题**：若遇到 SSL 错误，可添加 `-trusted-host` 参数（如方法一中所示）。
3. **镜像源稳定性**：不同镜像源可能有更新延迟，建议选择常用的镜像（如清华、阿里云）。

配置后，`uv venv` 安装依赖的速度会显著提升！