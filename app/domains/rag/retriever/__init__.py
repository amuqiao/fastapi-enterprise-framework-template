"""
RAG检索器模块
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
import json
import pandas as pd
from app.domains.rag.config import rag_config


class BaseRetriever(ABC):
    """检索器基类"""
    
    @abstractmethod
    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行检索
        
        Args:
            query: 查询文本
            **kwargs: 额外参数
            
        Returns:
            检索结果列表，每个结果包含文本、分数等信息
        """
        pass


class KeywordRetriever(BaseRetriever):
    """关键词检索器"""
    
    def __init__(self, index_dir: str):
        """
        初始化关键词检索器
        
        Args:
            index_dir: 索引目录
        """
        self.index_dir = index_dir
        self.keyword_index = {}
        self._load_index()
    
    def _load_index(self):
        """加载关键词索引"""
        # 简化实现，实际项目中可以使用更高效的索引结构
        index_file = os.path.join(self.index_dir, "keyword_index.json")
        
        # 首先尝试从 GraphRAG 生成的 Parquet 文件加载
        graphrag_output_dir = os.path.join(self.index_dir, "output")
        text_units_file = os.path.join(graphrag_output_dir, "create_final_text_units.parquet")
        documents_file = os.path.join(graphrag_output_dir, "create_final_documents.parquet")
        
        if os.path.exists(text_units_file):
            try:
                # 读取文本单元文件
                text_units_df = pd.read_parquet(text_units_file)
                documents_df = None
                
                # 读取文档文件（如果存在）
                if os.path.exists(documents_file):
                    documents_df = pd.read_parquet(documents_file)
                
                # 构建索引
                for idx, row in text_units_df.iterrows():
                    doc_id = f"doc_{idx}"
                    content = row.get("text", "")
                    metadata = {
                        "source": row.get("source", "graphrag"),
                        "document_id": row.get("document_id", ""),
                        "text_unit_id": row.get("id", "")
                    }
                    if documents_df is not None and not documents_df.empty:
                        # 尝试获取文档级别的元数据
                        doc_row = documents_df[documents_df["id"] == metadata["document_id"]]
                        if not doc_row.empty:
                            metadata["document_source"] = doc_row.iloc[0].get("source", "")
                
                    self.keyword_index[doc_id] = {
                        "content": content,
                        "metadata": metadata
                    }
                return
            except Exception as e:
                print(f"Error loading GraphRAG index: {e}")
        
        # 如果 GraphRAG 文件不存在或加载失败，尝试从 JSON 文件加载
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                self.keyword_index = json.load(f)
    
    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行关键词检索
        
        Args:
            query: 查询文本
            **kwargs: 额外参数
            
        Returns:
            检索结果列表
        """
        top_k = kwargs.get('top_k', rag_config.RETRIEVER_TOP_K)
        results = []
        
        # 简单的关键词匹配实现
        query_words = set(query.lower().split())
        for doc_id, doc_info in self.keyword_index.items():
            doc_content = doc_info.get('content', '').lower()
            doc_words = set(doc_content.split())
            common_words = query_words.intersection(doc_words)
            score = len(common_words) / (len(query_words) + 1)
            
            if score > 0:
                results.append({
                    'id': doc_id,
                    'content': doc_info.get('content', ''),
                    'score': score,
                    'metadata': doc_info.get('metadata', {})
                })
        
        # 如果没有结果，返回模拟结果（用于测试）
        if not results and len(self.keyword_index) > 0:
            for doc_id, doc_info in list(self.keyword_index.items())[:top_k]:
                results.append({
                    'id': doc_id,
                    'content': doc_info.get('content', ''),
                    'score': 0.5,
                    'metadata': doc_info.get('metadata', {})
                })
        
        # 按分数排序并返回前top_k个结果
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]


class VectorRetriever(BaseRetriever):
    """向量检索器"""
    
    def __init__(self, index_dir: str):
        """
        初始化向量检索器
        
        Args:
            index_dir: 索引目录
        """
        self.index_dir = index_dir
        self.vector_store = None
        self._init_vector_store()
    
    def _init_vector_store(self):
        """初始化向量存储"""
        # 这里应该根据配置初始化实际的向量存储
        # 简化实现，实际项目中需要集成真实的向量存储
        pass
    
    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行向量检索
        
        Args:
            query: 查询文本
            **kwargs: 额外参数
            
        Returns:
            检索结果列表
        """
        top_k = kwargs.get('top_k', rag_config.RETRIEVER_TOP_K)
        
        # 简化实现，实际项目中需要调用真实的向量存储进行检索
        # 这里返回模拟结果
        results = []
        for i in range(top_k):
            results.append({
                'id': f'doc_{i}',
                'content': f'示例文档内容 {i}，包含与查询相关的信息',
                'score': 0.8 - (i * 0.1),
                'metadata': {'source': 'example'}
            })
        return results


class HybridRetriever(BaseRetriever):
    """混合检索器"""
    
    def __init__(self, index_dir: str):
        """
        初始化混合检索器
        
        Args:
            index_dir: 索引目录
        """
        self.keyword_retriever = KeywordRetriever(index_dir)
        self.vector_retriever = VectorRetriever(index_dir)
        self.keyword_weight = 0.3
        self.vector_weight = 0.7
    
    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行混合检索
        
        Args:
            query: 查询文本
            **kwargs: 额外参数
            
        Returns:
            检索结果列表
        """
        top_k = kwargs.get('top_k', rag_config.RETRIEVER_TOP_K)
        
        # 执行关键词检索
        keyword_results = self.keyword_retriever.retrieve(query, **kwargs)
        
        # 执行向量检索
        vector_results = self.vector_retriever.retrieve(query, **kwargs)
        
        # 合并结果
        combined_results = {}
        for result in keyword_results:
            doc_id = result['id']
            combined_results[doc_id] = {
                'content': result['content'],
                'keyword_score': result['score'],
                'vector_score': 0,
                'metadata': result['metadata']
            }
        
        for result in vector_results:
            doc_id = result['id']
            if doc_id in combined_results:
                combined_results[doc_id]['vector_score'] = result['score']
            else:
                combined_results[doc_id] = {
                    'content': result['content'],
                    'keyword_score': 0,
                    'vector_score': result['score'],
                    'metadata': result['metadata']
                }
        
        # 计算综合分数
        for doc_id, doc_info in combined_results.items():
            doc_info['score'] = (
                doc_info['keyword_score'] * self.keyword_weight +
                doc_info['vector_score'] * self.vector_weight
            )
        
        # 按综合分数排序并返回前top_k个结果
        sorted_results = sorted(
            combined_results.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        # 格式化结果
        formatted_results = []
        for i, result in enumerate(sorted_results[:top_k]):
            formatted_results.append({
                'id': f'doc_{i}',
                'content': result['content'],
                'score': result['score'],
                'metadata': result['metadata']
            })
        
        return formatted_results


class RetrieverFactory:
    """检索器工厂类"""
    
    @staticmethod
    def create_retriever(retriever_type: str, index_dir: str) -> BaseRetriever:
        """
        创建检索器实例
        
        Args:
            retriever_type: 检索器类型，可选值：keyword, vector, hybrid
            index_dir: 索引目录
            
        Returns:
            检索器实例
        """
        if retriever_type == 'keyword':
            return KeywordRetriever(index_dir)
        elif retriever_type == 'vector':
            return VectorRetriever(index_dir)
        elif retriever_type == 'hybrid':
            return HybridRetriever(index_dir)
        else:
            raise ValueError(f"Unknown retriever type: {retriever_type}")