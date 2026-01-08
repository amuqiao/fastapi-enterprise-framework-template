#!/usr/bin/env python3
"""
示例脚本：打印项目信息
"""

import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import AppSettings, app_settings

def main():
    """脚本主函数"""
    print("=== 项目信息脚本 ===")
    print(f"Python 版本: {sys.version}")
    print(f"项目根目录: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    
    # 加载配置
    settings = AppSettings()
    print(f"配置环境: {settings.ENVIRONMENT}")
    print(f"API 版本: {settings.API_V1_STR}")
    
    print("=== 脚本执行完成 ===")

if __name__ == "__main__":
    main()