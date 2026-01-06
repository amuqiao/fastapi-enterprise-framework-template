"""
RAG生成器模块
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import requests
import json


class BaseGenerator(ABC):
    """生成器基类"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        执行生成
        
        Args:
            prompt: 提示词
            **kwargs: 额外参数
            
        Returns:
            生成的文本
        """
        pass


class OpenAIGenerator(BaseGenerator):
    """OpenAI生成器"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        初始化OpenAI生成器
        
        Args:
            api_key: OpenAI API密钥
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        使用OpenAI API执行生成
        
        Args:
            prompt: 提示词
            **kwargs: 额外参数
            
        Returns:
            生成的文本
        """
        temperature = kwargs.get('temperature', 0.1)
        max_tokens = kwargs.get('max_tokens', 1000)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"生成失败: {str(e)}"


class QwenGenerator(BaseGenerator):
    """Qwen在线模型生成器"""
    
    def __init__(self, api_key: str, model: str = "qwen-plus", base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"):
        """
        初始化Qwen生成器
        
        Args:
            api_key: Qwen API密钥
            model: 使用的模型名称
            base_url: API基础URL
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        使用Qwen API执行生成
        
        Args:
            prompt: 提示词
            **kwargs: 额外参数
            
        Returns:
            生成的文本
        """
        temperature = kwargs.get('temperature', 0.1)
        max_tokens = kwargs.get('max_tokens', 1000)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"生成失败: {str(e)}"


class MockGenerator(BaseGenerator):
    """模拟生成器，用于测试"""
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        执行模拟生成
        
        Args:
            prompt: 提示词
            **kwargs: 额外参数
            
        Returns:
            生成的文本
        """
        return f"模拟生成的回答：{prompt[:50]}..."


class GeneratorFactory:
    """生成器工厂类"""
    
    @staticmethod
    def create_generator(generator_type: str, **kwargs) -> BaseGenerator:
        """
        创建生成器实例
        
        Args:
            generator_type: 生成器类型，可选值：openai, qwen, mock
            **kwargs: 额外参数
            
        Returns:
            生成器实例
        """
        if generator_type == 'openai':
            api_key = kwargs.get('api_key')
            model = kwargs.get('model', 'gpt-3.5-turbo')
            return OpenAIGenerator(api_key, model)
        elif generator_type == 'qwen':
            api_key = kwargs.get('api_key')
            model = kwargs.get('model', 'qwen-plus')
            base_url = kwargs.get('base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions')
            return QwenGenerator(api_key, model, base_url)
        elif generator_type == 'mock':
            return MockGenerator()
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")