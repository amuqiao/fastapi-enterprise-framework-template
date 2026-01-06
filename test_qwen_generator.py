#!/usr/bin/env python3
"""
测试真实的qwen生成器
"""

import sys
import os
import json
from fastapi.testclient import TestClient

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import app

client = TestClient(app)


def test_qwen_generator():
    """测试qwen生成器"""
    print("测试真实的qwen生成器...")
    
    # 测试请求
    payload = {
        "query": "什么是RAG技术？",
        "index_name": "default",
        "top_k": 5,
        "retriever_type": "hybrid",
        "generator_type": "qwen",
        "prompt_template": "basic_search_system_prompt.txt"
    }
    
    # 发送请求
    response = client.post("/api/v1/rag/query", json=payload)
    
    # 打印响应状态码
    print(f"响应状态码: {response.status_code}")
    
    # 打印响应内容
    if response.status_code == 200:
        result = response.json()
        print("\n响应内容:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 检查是否是真实的生成结果
        answer = result.get('answer', '')
        if "模拟生成的回答" in answer:
            print("\n❌ 警告: 生成器返回的是模拟结果，不是真实的qwen生成结果")
        else:
            print("\n✅ 成功: 生成器返回的是真实的qwen生成结果")
    else:
        print(f"\n❌ 错误: {response.text}")


def test_qwen_generator_with_custom_prompt():
    """测试带自定义提示词的qwen生成器"""
    print("\n\n测试带自定义提示词的qwen生成器...")
    
    # 测试请求
    payload = {
        "query": "如何使用Python实现快速排序？",
        "index_name": "default",
        "top_k": 3,
        "retriever_type": "hybrid",
        "generator_type": "qwen",
        "prompt_template": "local_search_system_prompt.txt"
    }
    
    # 发送请求
    response = client.post("/api/v1/rag/query", json=payload)
    
    # 打印响应状态码
    print(f"响应状态码: {response.status_code}")
    
    # 打印响应内容
    if response.status_code == 200:
        result = response.json()
        print("\n响应内容:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 检查是否是真实的生成结果
        answer = result.get('answer', '')
        if "模拟生成的回答" in answer:
            print("\n❌ 警告: 生成器返回的是模拟结果，不是真实的qwen生成结果")
        else:
            print("\n✅ 成功: 生成器返回的是真实的qwen生成结果")
    else:
        print(f"\n❌ 错误: {response.text}")


if __name__ == "__main__":
    test_qwen_generator()
    test_qwen_generator_with_custom_prompt()
    print("\n\n测试完成！")