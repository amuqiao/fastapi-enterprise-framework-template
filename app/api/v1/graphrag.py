from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from pydantic import BaseModel
from app.services.graphrag_service import GraphRAGService
from app.dependencies.service import get_graphrag_service

router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求模型"""
    query: str


class ToolInfo(BaseModel):
    """工具信息模型"""
    name: str
    description: str
    parameters: Dict[str, Any]


class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    tool_info: List[ToolInfo]


class ToolListResponse(BaseModel):
    """工具列表响应模型"""
    tools: List[ToolInfo]


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    chat_request: ChatRequest,
    graphrag_service: GraphRAGService = Depends(get_graphrag_service)
):
    """GraphRAG聊天接口"""
    try:
        # 使用local search作为默认搜索方式
        result = await graphrag_service.local_asearch(chat_request.query)
        
        # 获取可用工具列表
        tools = graphrag_service.get_available_tools()
        
        # 转换为ToolInfo模型列表
        tool_infos = [ToolInfo(**tool) for tool in tools]
        
        return ChatResponse(
            response=result.response,
            tool_info=tool_infos
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"聊天请求处理失败: {str(e)}"
        )


@router.get("/tools", response_model=ToolListResponse, status_code=status.HTTP_200_OK)
async def get_tools(
    graphrag_service: GraphRAGService = Depends(get_graphrag_service)
):
    """获取可用工具列表"""
    try:
        # 获取可用工具列表
        tools = graphrag_service.get_available_tools()
        
        # 转换为ToolInfo模型列表
        tool_infos = [ToolInfo(**tool) for tool in tools]
        
        return ToolListResponse(tools=tool_infos)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取工具列表失败: {str(e)}"
        )
