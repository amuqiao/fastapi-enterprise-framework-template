"""
RAG API接口测试
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_rag_query():
    """测试RAG查询接口"""
    response = client.post("/api/v1/rag/query", json={"query": "测试查询"})
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "answer" in data


def test_list_indexes():
    """测试列出索引接口"""
    response = client.get("/api/v1/rag/indexes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_rag_query_with_params():
    """测试带参数的RAG查询接口"""
    response = client.post(
        "/api/v1/rag/query",
        json={
            "query": "测试查询",
            "index_name": "default",
            "top_k": 3,
            "retriever_type": "hybrid"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "answer" in data


def test_pipeline_config_update():
    """测试管道配置更新接口"""
    response = client.post(
        "/api/v1/rag/pipelines/config",
        params={
            "index_name": "default",
            "retriever_type": "hybrid",
            "generator_type": "mock"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])