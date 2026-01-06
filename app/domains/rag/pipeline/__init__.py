"""
RAG管道模块
"""

from typing import Dict, Any, Optional, List
from app.domains.rag.retriever import BaseRetriever, RetrieverFactory
from app.domains.rag.generator import BaseGenerator, GeneratorFactory
from app.domains.rag.prompt import PromptTemplateManager
from app.domains.rag.config import rag_config


class RAGPipeline:
    """RAG管道类"""
    
    def __init__(
        self,
        index_dir: str,
        retriever_type: str = 'hybrid',
        generator_type: str = 'mock',
        prompt_template: str = 'basic_search_system_prompt.txt',
        **kwargs
    ):
        """
        初始化RAG管道
        
        Args:
            index_dir: 索引目录
            retriever_type: 检索器类型
            generator_type: 生成器类型
            prompt_template: 提示词模板名称
            **kwargs: 额外参数
        """
        self.index_dir = index_dir
        self.retriever_type = retriever_type
        self.generator_type = generator_type
        self.prompt_template = prompt_template
        
        # 初始化组件
        self.retriever = RetrieverFactory.create_retriever(retriever_type, index_dir)
        self.generator = GeneratorFactory.create_generator(generator_type, **kwargs)
        
        # 初始化提示词模板管理器
        template_dir = kwargs.get('template_dir', rag_config.PROMPT_TEMPLATE_DIR)
        self.prompt_manager = PromptTemplateManager(template_dir)
    
    def run(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        运行RAG管道
        
        Args:
            query: 查询文本
            **kwargs: 额外参数
            
        Returns:
            包含检索结果和生成回答的字典
        """
        # 执行检索
        retrieval_results = self.retriever.retrieve(query, **kwargs)
        
        # 构建上下文
        context = "\n\n".join([result['content'] for result in retrieval_results])
        
        # 渲染提示词模板
        prompt = self.prompt_manager.render_template(
            self.prompt_template,
            context=context,
            question=query
        )
        
        if not prompt:
            # 如果模板渲染失败，使用默认提示词
            prompt = f"根据以下上下文回答问题：\n\n{context}\n\n问题：{query}\n\n回答："
        
        # 执行生成
        answer = self.generator.generate(prompt, **kwargs)
        
        # 返回结果
        return {
            'query': query,
            'retrieval_results': retrieval_results,
            'answer': answer,
            'context': context
        }
    
    def get_retriever(self) -> BaseRetriever:
        """
        获取检索器实例
        
        Returns:
            检索器实例
        """
        return self.retriever
    
    def get_generator(self) -> BaseGenerator:
        """
        获取生成器实例
        
        Returns:
            生成器实例
        """
        return self.generator
    
    def update_retriever(self, retriever_type: str, **kwargs) -> None:
        """
        更新检索器
        
        Args:
            retriever_type: 检索器类型
            **kwargs: 额外参数
        """
        self.retriever_type = retriever_type
        self.retriever = RetrieverFactory.create_retriever(retriever_type, self.index_dir)
    
    def update_generator(self, generator_type: str, **kwargs) -> None:
        """
        更新生成器
        
        Args:
            generator_type: 生成器类型
            **kwargs: 额外参数
        """
        self.generator_type = generator_type
        self.generator = GeneratorFactory.create_generator(generator_type, **kwargs)
    
    def update_prompt_template(self, prompt_template: str) -> None:
        """
        更新提示词模板
        
        Args:
            prompt_template: 提示词模板名称
        """
        self.prompt_template = prompt_template


class RAGPipelineFactory:
    """RAG管道工厂类"""
    
    @staticmethod
    def create_pipeline(index_dir: str, **kwargs) -> RAGPipeline:
        """
        创建RAG管道实例
        
        Args:
            index_dir: 索引目录
            **kwargs: 额外参数
            
        Returns:
            RAG管道实例
        """
        return RAGPipeline(index_dir, **kwargs)