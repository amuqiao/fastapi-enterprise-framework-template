"""
RAG配置管理模块
"""

from pydantic_settings import BaseSettings
from typing import Optional


class RAGConfig(BaseSettings):
    """RAG配置类"""
    # 索引相关配置
    INDEX_BASE_DIR: str = "./output"
    DEFAULT_INDEX_NAME: str = "default"
    
    # 检索器配置
    RETRIEVER_TOP_K: int = 5
    RETRIEVER_SCORE_THRESHOLD: float = 0.3
    
    # 向量存储配置
    VECTOR_STORE_TYPE: str = "lancedb"
    LANCEDB_DIR: str = "./output/lancedb"
    
    # 嵌入模型配置
    EMBEDDING_MODEL: str = "text-embedding-v2"
    EMBEDDING_API_KEY: Optional[str] = None
    
    # LLM配置
    LLM_MODEL: str = "qwen-plus"
    LLM_API_KEY: Optional[str] = "sk-9ec27f85396f41788a441841e6d4a718"
    LLM_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1000
    
    # 提示词模板配置
    PROMPT_TEMPLATE_DIR: str = "./app/domains/rag/prompt/templates"
    DEFAULT_PROMPT_TEMPLATE: str = "basic_search_system_prompt.txt"
    
    # 飞书机器人配置
    FEISHU_WEBHOOK_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的环境变量


# 创建全局配置实例
rag_config = RAGConfig()