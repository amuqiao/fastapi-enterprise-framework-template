"""
RAG API接口
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.domains.rag.services import rag_service
from app.dependencies.config import get_app_settings, AppSettings

# 创建路由器
router = APIRouter()


class RagQueryRequest(BaseModel):
    """RAG查询请求模型"""
    query: str = Field(..., description="查询文本", example="什么是RAG技术？")
    index_name: str = Field("default", description="索引名称", example="default")
    top_k: int = Field(5, description="返回结果数量", ge=1, le=20, example=5)
    retriever_type: Optional[str] = Field(None, description="检索器类型", example="hybrid")
    generator_type: Optional[str] = Field(None, description="生成器类型", example="qwen")
    prompt_template: Optional[str] = Field(None, description="提示词模板", example="basic_search_system_prompt.txt")


@router.post("/query", response_model=Dict[str, Any], summary="执行RAG查询")
async def rag_query(
    request: RagQueryRequest,
    app_settings: AppSettings = Depends(get_app_settings)
) -> Dict[str, Any]:
    """
    RAG查询接口
    
    示例请求:
    ```json
    {
        "query": "什么是RAG技术？",
        "index_name": "default",
        "top_k": 5,
        "retriever_type": "hybrid",
        "generator_type": "qwen",
        "prompt_template": "basic_search_system_prompt.txt"
    }
    ```
    
    示例响应:
    ```json
    {
        "query": "什么是RAG技术？",
        "retrieval_results": [
            {
                "id": "doc_0",
                "content": "示例文档内容 0，包含与查询相关的信息",
                "score": 0.8,
                "metadata": {"source": "example"}
            }
        ],
        "answer": "RAG（Retrieval-Augmented Generation）是一种结合了检索和生成的人工智能技术...",
        "context": "示例文档内容 0，包含与查询相关的信息"
    }
    ```
    
    Args:
        request: 查询请求数据
        app_settings: 应用设置
        
    Returns:
        查询结果
    """
    try:
        # 构建参数
        kwargs = {
            'top_k': request.top_k,
        }
        
        # 如果指定了检索器类型，先更新管道配置
        if request.retriever_type or request.generator_type or request.prompt_template:
            rag_service.update_pipeline_config(
                request.index_name,
                request.retriever_type,
                request.generator_type,
                request.prompt_template
            )
        
        # 执行查询
        result = rag_service.query(request.query, request.index_name, **kwargs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/indexes", response_model=List[str], summary="列出所有可用的索引")
async def list_indexes(
    app_settings: AppSettings = Depends(get_app_settings)
) -> List[str]:
    """
    列出所有可用的索引
    
    示例响应:
    ```json
    ["default", "doupocangqiong", "生产故障经验问答"]
    ```
    
    Args:
        app_settings: 应用设置
        
    Returns:
        索引名称列表
    """
    try:
        indexes = rag_service.list_indexes()
        return indexes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取索引列表失败: {str(e)}")


@router.post("/pipelines/config", response_model=Dict[str, Any], summary="更新管道配置")
async def update_pipeline_config(
    index_name: str = Query(..., description="索引名称", example="default"),
    retriever_type: Optional[str] = Query(None, description="检索器类型", example="hybrid"),
    generator_type: Optional[str] = Query(None, description="生成器类型", example="qwen"),
    prompt_template: Optional[str] = Query(None, description="提示词模板", example="basic_search_system_prompt.txt"),
    app_settings: AppSettings = Depends(get_app_settings)
) -> Dict[str, Any]:
    """
    更新管道配置
    
    示例请求:
    ```
    POST /api/v1/rag/pipelines/config?index_name=default&retriever_type=hybrid&generator_type=qwen
    ```
    
    示例响应:
    ```json
    {
        "success": true,
        "message": "管道配置更新成功"
    }
    ```
    
    Args:
        index_name: 索引名称
        retriever_type: 检索器类型
        generator_type: 生成器类型
        prompt_template: 提示词模板
        app_settings: 应用设置
        
    Returns:
        更新结果
    """
    try:
        success = rag_service.update_pipeline_config(
            index_name,
            retriever_type,
            generator_type,
            prompt_template
        )
        return {
            "success": success,
            "message": "管道配置更新成功" if success else "管道配置更新失败"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新管道配置失败: {str(e)}")


@router.get("/generators", response_model=List[str], summary="列出所有可用的生成器类型")
async def list_generators() -> List[str]:
    """
    列出所有可用的生成器类型
    
    示例响应:
    ```json
    ["mock", "openai", "qwen"]
    ```
    
    Returns:
        生成器类型列表
    """
    return ["mock", "openai", "qwen"]


@router.get("/retrievers", response_model=List[str], summary="列出所有可用的检索器类型")
async def list_retrievers() -> List[str]:
    """
    列出所有可用的检索器类型
    
    示例响应:
    ```json
    ["keyword", "vector", "hybrid"]
    ```
    
    Returns:
        检索器类型列表
    """
    return ["keyword", "vector", "hybrid"]