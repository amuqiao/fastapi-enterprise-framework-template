"""
提示词模板管理模块
"""

import os
from typing import Dict, Optional, Union


class PromptTemplateManager:
    """提示词模板管理器"""
    
    def __init__(self, template_dir: str):
        """
        初始化提示词模板管理器
        
        Args:
            template_dir: 提示词模板目录
        """
        self.template_dir = template_dir
        self.templates: Dict[str, str] = {}
        self._load_templates()
    
    def _load_templates(self):
        """加载所有提示词模板"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir, exist_ok=True)
        
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.txt'):
                template_path = os.path.join(self.template_dir, filename)
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.templates[filename] = content
    
    def get_template(self, template_name: str) -> Optional[str]:
        """
        获取指定的提示词模板
        
        Args:
            template_name: 模板名称，包括文件扩展名
            
        Returns:
            提示词模板内容，如果不存在返回None
        """
        return self.templates.get(template_name)
    
    def get_template_by_name(self, template_name: str) -> Optional[str]:
        """
        根据模板名称（不含扩展名）获取提示词模板
        
        Args:
            template_name: 模板名称，不含文件扩展名
            
        Returns:
            提示词模板内容，如果不存在返回None
        """
        for filename, content in self.templates.items():
            if filename.startswith(template_name) and filename.endswith('.txt'):
                return content
        return None
    
    def render_template(self, template_name: str, **kwargs) -> Optional[str]:
        """
        渲染提示词模板，替换模板中的变量
        
        Args:
            template_name: 模板名称
            **kwargs: 要替换的变量
            
        Returns:
            渲染后的提示词内容，如果模板不存在返回None
        """
        template = self.get_template(template_name)
        if template:
            return template.format(**kwargs)
        return None
    
    def add_template(self, template_name: str, content: str) -> bool:
        """
        添加新的提示词模板
        
        Args:
            template_name: 模板名称，包括文件扩展名
            content: 模板内容
            
        Returns:
            是否添加成功
        """
        try:
            template_path = os.path.join(self.template_dir, template_name)
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.templates[template_name] = content
            return True
        except Exception:
            return False
    
    def list_templates(self) -> list:
        """
        列出所有可用的提示词模板
        
        Returns:
            模板名称列表
        """
        return list(self.templates.keys())


# 默认提示词模板
DEFAULT_TEMPLATES = {
    "basic_search_system_prompt.txt": """你是一个专业的知识库问答助手，你的任务是根据提供的上下文信息回答用户的问题。

**工作原则：**
1. 严格基于提供的上下文信息回答问题，不要添加任何外部信息
2. 如果上下文信息不足以回答问题，明确表示无法回答
3. 保持回答准确、简洁、专业
4. 对于复杂问题，分步骤清晰回答

**上下文信息：**
{context}

**用户问题：**
{question}

**回答：**
""",
    "local_search_system_prompt.txt": """你是一个专业的知识库问答助手，专注于本地知识库的检索和回答。

**工作原则：**
1. 严格基于提供的本地知识库上下文信息回答问题
2. 优先使用最相关的信息，确保回答的准确性
3. 保持回答简洁明了，直接针对用户问题
4. 如果无法从上下文获取足够信息，明确表示无法回答

**本地知识库上下文：**
{context}

**用户问题：**
{question}

**回答：**
""",
    "global_search_system_prompt.txt": """你是一个全局知识库问答助手，能够综合分析多个知识源的信息。

**工作原则：**
1. 综合分析提供的所有上下文信息
2. 识别信息之间的关联和一致性
3. 基于综合分析给出全面、准确的回答
4. 保持回答结构清晰，逻辑连贯

**全局知识库上下文：**
{context}

**用户问题：**
{question}

**回答：**
""",
    "drift_search_system_prompt.txt": """你是一个高级知识库问答助手，能够处理复杂的知识检索和推理任务。

**工作原则：**
1. 深入分析提供的上下文信息
2. 识别关键概念和实体之间的关系
3. 基于分析进行合理的推理和扩展
4. 给出详细、准确、有深度的回答

**知识库上下文：**
{context}

**用户问题：**
{question}

**回答：**
""",
}


def init_default_templates(template_dir: str):
    """
    初始化默认提示词模板
    
    Args:
        template_dir: 模板目录
    """
    if not os.path.exists(template_dir):
        os.makedirs(template_dir, exist_ok=True)
    
    for filename, content in DEFAULT_TEMPLATES.items():
        template_path = os.path.join(template_dir, filename)
        if not os.path.exists(template_path):
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)