def test_graphrag_chat(client):
    """测试GraphRAG聊天接口"""
    response = client.post(
        "/api/v1/graphrag/chat",
        json={
            "query": "萧炎的父亲是谁?"
        }
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "tool_info" in response.json()
    assert isinstance(response.json()["response"], str)
    assert isinstance(response.json()["tool_info"], list)
    # 检查返回的工具列表长度
    assert len(response.json()["tool_info"]) > 0


def test_graphrag_get_tools(client):
    """测试获取GraphRAG可用工具列表"""
    response = client.get("/api/v1/graphrag/tools")
    
    assert response.status_code == 200
    assert "tools" in response.json()
    assert isinstance(response.json()["tools"], list)
    # 检查返回的工具列表长度
    assert len(response.json()["tools"]) > 0
    
    # 检查每个工具的结构
    for tool in response.json()["tools"]:
        assert "name" in tool
        assert "description" in tool
        assert "parameters" in tool
        assert isinstance(tool["name"], str)
        assert isinstance(tool["description"], str)
        assert isinstance(tool["parameters"], dict)


def test_graphrag_chat_invalid_input(client):
    """测试GraphRAG聊天接口无效输入"""
    # 测试空查询
    response = client.post(
        "/api/v1/graphrag/chat",
        json={
            "query": ""
        }
    )
    
    # 应该返回422 Unprocessable Entity，因为query是必填字段且不能为空
    assert response.status_code == 422
    
    # 测试缺少query字段
    response = client.post(
        "/api/v1/graphrag/chat",
        json={}
    )
    
    # 应该返回422 Unprocessable Entity，因为缺少必填字段query
    assert response.status_code == 422
