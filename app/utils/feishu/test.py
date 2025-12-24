
import requests

# 获取企业级访问令牌
def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    else:
        print(f"获取令牌失败: {result.get('msg')}")
        return None

# 获取文档列表
def list_files(token):
    url = "https://open.feishu.cn/open-apis/drive/v1/files"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"direction": "DESC", "order_by": "EditedTime"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 测试API连接性
def test_api_connection(token):
    """测试基本的API连接性"""
    print("\n🔍 正在测试API连接性...")
    
    # 测试获取当前应用信息（这个通常只需要基础权限）
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/verify"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            print("✅ API连接性测试成功！")
            print(f"   - 应用ID: {result.get('app_id')}")
            print(f"   - Token类型: {result.get('token_type')}")
            return True
        else:
            print(f"❌ API连接性测试失败: {result.get('msg')}")
    else:
        print(f"❌ API连接性测试HTTP错误: {response.status_code} - {response.text}")
    
    return False

# 打印权限申请建议
def print_permission_suggestions(error_msg):
    """打印权限申请建议"""
    print("\n💡 权限申请建议:")
    print("1. 登录飞书开放平台: https://open.feishu.cn")
    print("2. 进入应用详情页")
    print("3. 点击左侧菜单中的\"权限管理\"")
    print("4. 申请以下任一权限:")
    print("   - drive:drive")
    print("   - drive:drive:readonly")
    print("   - space:document:retrieve")
    print("5. 提交申请并等待管理员审批")
    print("\n📋 也可以直接访问以下链接申请权限:")
    print("   https://open.feishu.cn/app/cli_a9c10defa47c9bd3/auth?q=drive:drive,drive:drive:readonly,space:document:retrieve&op_from=openapi&token_type=tenant")

# 示例
if __name__ == "__main__":
    app_id = "cli_a9c10defa47c9bd3"
    app_secret = "hZVeJ10fCRn5dOtZh9FRRhHDU2alnsh1"
    
    print("📋 正在获取飞书访问令牌...")
    token = get_tenant_access_token(app_id, app_secret)
    
    if token:
        print(f"✅ 成功获取访问令牌: {token}")
        
        # 测试API连接性
        test_api_connection(token)
        
        # 尝试获取文档列表
        print("\n📁 正在获取飞书文档列表...")
        files = list_files(token)
        
        if files.get("code") == 0:
            file_list = files.get("data", {}).get("files", [])
            print(f"✅ 成功获取 {len(file_list)} 个文档")
            
            if file_list:
                print("\n📋 文档列表:")
                print("-" * 60)
                for i, file in enumerate(file_list, 1):
                    print(f"{i}. 名称: {file.get('name', '未知')}")
                    print(f"   类型: {file.get('type', '未知')}")
                    print(f"   Token: {file.get('token', '未知')}")
                    print(f"   创建时间: {file.get('create_time', '未知')}")
                    print(f"   更新时间: {file.get('update_time', '未知')}")
                    print("-" * 60)
        else:
            error_code = files.get("code")
            error_msg = files.get("msg")
            print(f"❌ 获取文档列表失败: {error_msg}")
            
            # 根据错误码提供具体建议
            if error_code == 99991672:
                print_permission_suggestions(error_msg)
            elif error_code == 404:
                print("\n💡 建议: 检查API端点是否正确，或者文档是否存在")
            elif error_code == 401:
                print("\n💡 建议: 检查Token是否有效，可能已过期")
            
            print(f"\n详细错误信息: {files}")
    else:
        print("❌ 无法获取访问令牌，程序终止")
        print("\n💡 建议:")
        print("1. 检查App ID和App Secret是否正确")
        print("2. 检查网络连接是否正常")
        print("3. 检查飞书开放平台是否有相关服务故障")

