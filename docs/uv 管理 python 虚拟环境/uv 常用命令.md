强制 `uv` 重新安装所有依赖，我们需要删除现有的锁文件并使用重新安装选项。

```bash
rm -f uv.lock 
uv sync --force-reinstall
```

如果您想要更彻底地重新安装，可以先清理 uv 的缓存目录

```bash
uv cache clean
```