- 报错

```bash
(.venv) ➜  fastapi-enterprise-framework-template git:(graph_rag_mcp_agent) ✗ uv add graphrag-more==1.2.0
Resolved 121 packages in 143ms
      Built fastapi-enterprise-template @ file:///Users/wangqiao/Downloads/github_project/fastapi-enterprise-framework-template
  × Failed to build `llvmlite==0.46.0`
  ├─▶ The build backend returned an error
  ╰─▶ Call to `setuptools.build_meta:__legacy__.build_wheel` failed (exit status: 1)

      [stdout]
      running bdist_wheel
      /Users/wangqiao/.cache/uv/builds-v0/.tmpIVxBaC/bin/python
      /Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi/build.py
      -- Configuring incomplete, errors occurred!
      Running: cmake -G Unix Makefiles /Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi

      [stderr]
      CMake Error at CMakeLists.txt:21 (find_package):
        Could not find a package configuration file provided by "LLVM" with any of
        the following names:

          LLVMConfig.cmake
          llvm-config.cmake

        Add the installation prefix of "LLVM" to CMAKE_PREFIX_PATH or set
        "LLVM_DIR" to a directory containing one of the above files.  If "LLVM"
        provides a separate development package or SDK, be sure it has been
        installed.

      
      Traceback (most recent call last):
        File "/Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi/build.py", line 209,
      in <module>
          main()
        File "/Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi/build.py", line 203,
      in main
          main_posix('.dylib')
        File "/Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi/build.py", line 189,
      in main_posix
          try_cmake(here_dir, build_dir, generator)
        File "/Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi/build.py", line 127,
      in try_cmake
          subprocess.check_call(args)
        File "/Users/wangqiao/.local/share/uv/python/cpython-3.11.11-macos-x86_64-none/lib/python3.11/subprocess.py", line
      413, in check_call
          raise CalledProcessError(retcode, cmd)
      subprocess.CalledProcessError: Command '['cmake', '-G', 'Unix Makefiles',
      '/Users/wangqiao/.cache/uv/sdists-v9/pypi/llvmlite/0.46.0/Z4-wsxCvp7LQ7wkrJQsdw/src/ffi']' returned non-zero exit
      status 1.
      error: command '/Users/wangqiao/.cache/uv/builds-v0/.tmpIVxBaC/bin/python' failed with exit code 1

      hint: This usually indicates a problem with the package or the build environment.
  help: If you want to add the package regardless of the failed resolution, provide the `--frozen` flag to skip locking
        and syncing.
```

- 解决方案

```bash
brew install llvm 
brew install swig
由于Homebrew安装LLVM时遇到了swig下载问题，我将尝试使用预编译的llvmlite版本。我将使用--prefer-binary选项来优先使用预编译包。
UV_EXTRA_INDEX_URL=https://pypi.org/simple uv add llvmlite==0.46.0 --prefer-binary 
uv不支持--prefer-binary选项，我将尝试使用pip直接安装预编译的llvmlite轮包，使用--only-binary选项确保只使用预编译版本。
```

- 具体步骤

我需要总结在macOS上安装graphrag-more时遇到的错误及解决方法。在macOS上安装graphrag-more时，主要遇到了以下问题及解决方法：

### 遇到的错误

1. **缺少LLVM依赖**：安装graphrag-more时，其依赖的llvmlite库需要系统级的LLVM依赖，而macOS默认没有安装LLVM开发库。
2. **llvmlite构建失败**：由于缺少LLVM，导致llvmlite在构建过程中无法找到LLVM配置文件（LLVMConfig.cmake或llvm-config.cmake）。
3. **Homebrew安装LLVM遇到网络问题**：尝试使用Homebrew安装LLVM时，无法下载依赖的swig包。

### 解决方法

1. **安装预编译的llvmlite版本**：使用pip的`-only-binary :all:`选项安装预编译的llvmlite版本，避免从源码构建：
    
    ```
    python -m pip install llvmlite==0.45.0 --only-binary :all:
    
    ```
    
2. **跳过llvmlite构建**：通过安装预编译的llvmlite版本，然后再安装graphrag，从而跳过llvmlite的构建过程：
    
    ```
    python -m pip install graphrag
    
    ```
    
3. **配置环境变量**：在尝试从源码构建llvmlite时，可以设置LLVM_DIR环境变量指向LLVM的安装路径：
    
    ```
    export LLVM_DIR=$(brew --prefix llvm)/lib/cmake/llvm
    
    ```
    
4. **使用不同版本的llvmlite**：如果最新版本的llvmlite构建失败，可以尝试安装较旧的稳定版本，如0.45.0，这些版本通常有预编译的wheel包。

### 最终解决方案

经过多次尝试，最终成功的解决方案是：

1. 安装预编译的llvmlite版本（0.45.0）
2. 然后直接安装graphrag包

这种方法避免了从源码构建llvmlite，从而绕过了LLVM依赖问题。

### 建议

1. 在macOS上安装需要系统依赖的Python库时，优先考虑使用预编译的wheel包
2. 对于依赖复杂系统库的包，可以考虑使用conda或docker来管理环境
3. 遇到构建失败时，检查是否有预编译版本可用，或尝试使用较旧的稳定版本
4. 可以通过设置环境变量来指定系统库的位置，帮助构建过程找到所需的依赖

通过以上方法，我们成功解决了在macOS上安装graphrag-more时遇到的问题，完成了GraphRAG+MCP+RAG功能到现有FastAPI项目的集成。