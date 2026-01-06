"""
RAG服务模块
"""

from typing import Dict, Any, Optional
from app.domains.rag.pipeline import RAGPipeline, RAGPipelineFactory
from app.domains.rag.config import rag_config


class RAGService:
    """RAG服务类"""
    
    def __init__(self):
        """初始化RAG服务"""
        self.pipelines = {}
        self._init_pipelines()
    
    def _init_pipelines(self):
        """初始化RAG管道"""
        # 为默认索引创建管道
        default_index_dir = rag_config.INDEX_BASE_DIR
        self.pipelines['default'] = RAGPipelineFactory.create_pipeline(default_index_dir)
    
    def get_pipeline(self, index_name: str = 'default') -> Optional[RAGPipeline]:
        """
        获取指定索引的RAG管道
        
        Args:
            index_name: 索引名称
            
        Returns:
            RAG管道实例，如果不存在返回None
        """
        if index_name not in self.pipelines:
            # 动态创建管道
            index_dir = f"{rag_config.INDEX_BASE_DIR}/{index_name}"
            self.pipelines[index_name] = RAGPipelineFactory.create_pipeline(index_dir)
        return self.pipelines[index_name]
    
    def query(self, query: str, index_name: str = 'default', **kwargs) -> Dict[str, Any]:
        """
        执行RAG查询
        
        Args:
            query: 查询文本
            index_name: 索引名称
            **kwargs: 额外参数
            
        Returns:
            查询结果
        """
        pipeline = self.get_pipeline(index_name)
        if pipeline:
            return pipeline.run(query, **kwargs)
        else:
            return {
                'query': query,
                'error': f"索引 {index_name} 不存在",
                'answer': f"无法查询索引 {index_name}"
            }
    
    def list_indexes(self) -> list:
        """
        列出所有可用的索引
        
        Returns:
            索引名称列表
        """
        import os
        indexes = ['default']
        if os.path.exists(rag_config.INDEX_BASE_DIR):
            for item in os.listdir(rag_config.INDEX_BASE_DIR):
                item_path = os.path.join(rag_config.INDEX_BASE_DIR, item)
                if os.path.isdir(item_path):
                    indexes.append(item)
        return list(set(indexes))
    
    def update_pipeline_config(
        self,
        index_name: str,
        retriever_type: Optional[str] = None,
        generator_type: Optional[str] = None,
        prompt_template: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        更新管道配置
        
        Args:
            index_name: 索引名称
            retriever_type: 检索器类型
            generator_type: 生成器类型
            prompt_template: 提示词模板
            **kwargs: 额外参数
            
        Returns:
            是否更新成功
        """
        pipeline = self.get_pipeline(index_name)
        if pipeline:
            if retriever_type:
                pipeline.update_retriever(retriever_type, **kwargs)
            if generator_type:
                # 如果是qwen生成器，添加必要的参数
                if generator_type == 'qwen':
                    kwargs['api_key'] = rag_config.LLM_API_KEY
                    kwargs['model'] = rag_config.LLM_MODEL
                    # 为qwen生成器添加正确的base_url
                    from app.domains.rag.generator import GeneratorFactory
                    # 直接创建新的qwen生成器并替换
                    new_generator = GeneratorFactory.create_generator(
                        generator_type,
                        api_key=rag_config.LLM_API_KEY,
                        model=rag_config.LLM_MODEL,
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
                    )
                    pipeline.generator = new_generator
                else:
                    pipeline.update_generator(generator_type, **kwargs)
            if prompt_template:
                pipeline.update_prompt_template(prompt_template)
            return True
        return False


# 创建全局RAG服务实例
rag_service = RAGService()