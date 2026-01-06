"""
RAG模块初始化
"""

from app.domains.rag.config import RAGConfig, rag_config
from app.domains.rag.services import RAGService, rag_service
from app.domains.rag.prompt import init_default_templates


# 初始化默认提示词模板
init_default_templates(rag_config.PROMPT_TEMPLATE_DIR)


__all__ = [
    'RAGConfig',
    'rag_config',
    'RAGService',
    'rag_service'
]