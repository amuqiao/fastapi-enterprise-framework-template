# uv 工具简介

uv 是集成虚拟环境管理与依赖编译的工具，简化了 pip-tools 使用流程。其核心通过 uv pip compile 子命令调用 pip-compile，实现依赖编译。

# 核心文件与参数

1. **`requirements.in`**：作为输入文件，仅记录顶层依赖（如 sphinx、myst-parser 等），便于快速定义项目核心需求。
2. **`-universal`**：若项目需同时兼容 Python 2 和 Python 3，添加此参数可确保生成的依赖清单适配双版本环境。
3. **`-output-file`**：指定编译后的依赖清单输出路径，如 --output-file docs/requirements.txt，生成的 requirements.txt 会包含所有依赖及其精确版本，锁定环境配置。

# 使用流程

## **安装 uv**

根据官方文档或包管理工具，在系统中安装 uv 工具，确保其正常运行。

## **项目初始化与虚拟环境创建**

```bash
cd uv_test_project
uv init uv_test
Initialized project `uv-test` at `/Users/wangqiao/Documents/github_project/uv_test_project/uv_test`

cd uv_test
# uv venv .venv --python=3.12(可选命令)
uv venv 
```

- `uv init uv_test` 会在项目目录下创建`uv_test/.python-version`,若存在`.python-version`并在其中指定了python版本`，则uv venv`时不用指定版本

## **定义依赖**

在 `docs/requirements.in` 中列出文档构建等所需的顶层依赖，示例：

```bash
# docs/requirements.in
sphinx
myst-parser
sphinx-rtd-theme
```

## **编译依赖**

```bash
uv pip compile docs/requirements.in --output-file docs/requirements.txt
```

此命令将解析 `requirements.in` 中的顶层依赖，递归计算所有传递依赖，并锁定精确版本，生成 `requirements.txt`。

## **安装依赖**

```bash
uv pip install -r docs/requirements.txt
```

通过锁定版本的 requirements.txt 安装依赖，保障团队成员环境一致性，避免因依赖版本差异导致的运行问题。

# 使用优势

1. **精确依赖管理**：`requirements.in` 聚焦顶层需求，`requirements.txt` 锁定全量精确版本，确保环境一致性。
2. **保障构建稳定**：避免因文档构建工具（如 Sphinx）版本差异导致的生成失败或格式错乱。
3. **提升协作效率**：团队共享 `requirements.txt`，消除 “在我机器上能运行” 的环境差异问题。

# 补充说明

1. **依赖更新**：当 requirements.in 中顶层依赖版本需更新时，重新执行 uv pip compile 命令，会根据新版本计算并更新 requirements.txt 中的所有依赖版本。
2. **多环境管理**：若项目存在多个不同功能的依赖需求（如开发、测试、生产），可分别创建对应 [requirements.in](http://requirements.in/) 文件，编译生成独立的 requirements.txt，按需安装。

以上系统梳理了 uv 使用requirements.in管理依赖的流程。若你对某部分还有疑问，或想补充特定场景使用，可随时告诉我。