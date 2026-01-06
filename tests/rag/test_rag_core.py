"""
RAG核心功能测试
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.domains.rag.config import RAGConfig, rag_config
from app.domains.rag.retriever import KeywordRetriever, VectorRetriever, HybridRetriever
from app.domains.rag.generator import MockGenerator
from app.domains.rag.prompt import PromptTemplateManager
from app.domains.rag.pipeline import RAGPipeline
from app.domains.rag.services import rag_service


def test_rag_config():
    """测试RAG配置"""
    assert isinstance(rag_config, RAGConfig)
    assert rag_config.INDEX_BASE_DIR == "./output"
    assert rag_config.RETRIEVER_TOP_K == 5
    assert rag_config.VECTOR_STORE_TYPE == "lancedb"


def test_keyword_retriever():
    """测试关键词检索器"""
    # 创建临时索引目录
    import tempfile
    import json
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试索引文件
        test_index = {
            "doc1": {
                "content": "这是一个测试文档，包含关键词测试和文档",
                "metadata": {"source": "test"}
            },
            "doc2": {
                "content": "这是另一个文档，包含关键词另一个",
                "metadata": {"source": "test"}
            }
        }
        
        index_file = os.path.join(temp_dir, "keyword_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(test_index, f)
        
        # 测试检索器
        retriever = KeywordRetriever(temp_dir)
        results = retriever.retrieve("测试文档")
        
        assert len(results) > 0
        assert results[0]['score'] > 0


def test_vector_retriever():
    """测试向量检索器"""
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        retriever = VectorRetriever(temp_dir)
        results = retriever.retrieve("测试查询")
        
        assert len(results) > 0
        assert all('score' in result for result in results)


def test_hybrid_retriever():
    """测试混合检索器"""
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        retriever = HybridRetriever(temp_dir)
        results = retriever.retrieve("测试查询")
        
        assert len(results) > 0
        assert all('score' in result for result in results)


def test_prompt_template_manager():
    """测试提示词模板管理器"""
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试模板文件
        template_content = "根据以下上下文回答问题：\n\n{context}\n\n问题：{question}\n\n回答："
        template_file = os.path.join(temp_dir, "test_template.txt")
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # 测试模板管理器
        manager = PromptTemplateManager(temp_dir)
        rendered = manager.render_template(
            "test_template.txt",
            context="这是测试上下文",
            question="这是测试问题"
        )
        
        assert rendered is not None
        assert "这是测试上下文" in rendered
        assert "这是测试问题" in rendered


def test_rag_pipeline():
    """测试RAG管道"""
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试模板目录
        template_dir = os.path.join(temp_dir, "templates")
        os.makedirs(template_dir, exist_ok=True)
        
        # 创建测试模板
        template_content = "根据以下上下文回答问题：\n\n{context}\n\n问题：{question}\n\n回答："
        template_file = os.path.join(template_dir, "basic_search_system_prompt.txt")
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # 测试管道
        pipeline = RAGPipeline(
            temp_dir,
            retriever_type="hybrid",
            generator_type="mock",
            template_dir=template_dir
        )
        
        result = pipeline.run("测试查询")
        
        assert result is not None
        assert 'query' in result
        assert 'retrieval_results' in result
        assert 'answer' in result
        assert 'context' in result


def test_rag_service():
    """测试RAG服务"""
    # 测试查询功能
    result = rag_service.query("测试查询")
    assert result is not None
    assert 'query' in result
    assert 'answer' in result
    
    # 测试列出索引
    indexes = rag_service.list_indexes()
    assert isinstance(indexes, list)
    assert len(indexes) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])