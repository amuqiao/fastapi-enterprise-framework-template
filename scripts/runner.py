#!/usr/bin/env python3
"""
脚本运行器：统一管理和执行脚本
"""

import os
import sys
import importlib.util

def main():
    """
    脚本运行器主函数
    用法：run-script <script_name>
    """
    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.py")
        
        if os.path.exists(script_path):
            # 添加项目根目录到 Python 路径
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # 加载并执行脚本
            spec = importlib.util.spec_from_file_location(script_name, script_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[script_name] = module
            spec.loader.exec_module(module)
            
            # 执行脚本的 main 函数
            if hasattr(module, "main"):
                module.main()
            else:
                print(f"脚本 {script_name} 没有 main 函数")
        else:
            print(f"找不到脚本 {script_name}")
            list_scripts()
    else:
        print("请指定要运行的脚本名称")
        list_scripts()

def list_scripts():
    """列出所有可用的脚本"""
    scripts_dir = os.path.dirname(__file__)
    print("可用脚本:")
    for file in os.listdir(scripts_dir):
        if file.endswith(".py") and file != "__init__.py" and file != "runner.py":
            print(f"  - {file[:-3]}")

if __name__ == "__main__":
    main()