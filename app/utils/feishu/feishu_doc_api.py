import requests
import re

# 飞书应用凭证配置
APP_ID = "cli_a9c10defa47c9bd3"
APP_SECRET = "hZVeJ10fCRn5dOtZh9FRRhHDU2alnsh1"

class FeishuDocAPI:
    """
    飞书文档API客户端，用于获取飞书文档数据
    """
    
    def __init__(self, app_id: str = APP_ID, app_secret: str = APP_SECRET):
        """
        初始化飞书文档API客户端
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
    
    def get_tenant_access_token(self) -> str:
        """
        获取企业级访问令牌
        
        Returns:
            str: 企业级访问令牌
        
        Raises:
            Exception: 获取令牌失败时抛出异常
        """
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                self.tenant_access_token = result["tenant_access_token"]
                return self.tenant_access_token
            else:
                raise Exception(f"获取令牌失败：{result.get('msg')}")
        else:
            raise Exception(f"获取令牌失败：HTTP {response.status_code} - {response.text}")
    
    def extract_file_id_from_url(self, url: str) -> str:
        """
        从飞书文档URL中提取file_id
        
        Args:
            url: 飞书文档URL
            
        Returns:
            str: 文档的file_id
            
        Raises:
            Exception: URL格式不正确时抛出异常
        """
        # 匹配飞书文档URL中的file_id
        patterns = [
            r"docs/docx([a-zA-Z0-9]+)",  # 普通文档
            r"docs/sheets([a-zA-Z0-9]+)",  # 表格
            r"base/([a-zA-Z0-9]+)",  # 多维表格
            r"wiki/([a-zA-Z0-9]+)",  # 知识库文档
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise Exception(f"无法从URL中提取file_id：{url}")
    
    def get_doc_content(self, file_id: str) -> dict:
        """
        获取普通文档（Doc）的内容
        
        Args:
            file_id: 文档的file_id
            
        Returns:
            dict: 文档的结构化内容
            
        Raises:
            Exception: 获取文档内容失败时抛出异常
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/drive/v2/files/{file_id}/content"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                return result["data"]
            else:
                raise Exception(f"获取文档内容失败：{result.get('msg')}")
        else:
            raise Exception(f"获取文档内容失败：HTTP {response.status_code} - {response.text}")
    
    def get_sheet_values(self, spreadsheet_id: str, sheet_id: str, range: str = None) -> dict:
        """
        获取表格（Sheet）的单元格数据
        
        Args:
            spreadsheet_id: 表格的spreadsheet_id
            sheet_id: 工作表的sheet_id
            range: 查询范围，如"A1:B10"（可选）
            
        Returns:
            dict: 表格的单元格数据
            
        Raises:
            Exception: 获取表格数据失败时抛出异常
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_id}/sheets/{sheet_id}/values"
        if range:
            url += f"?range={range}"
        
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                return result["data"]
            else:
                raise Exception(f"获取表格数据失败：{result.get('msg')}")
        else:
            raise Exception(f"获取表格数据失败：HTTP {response.status_code} - {response.text}")
    
    def get_bitable_records(self, app_id: str, table_id: str, page_size: int = 100) -> dict:
        """
        获取多维表格（Bitable）的记录数据
        
        Args:
            app_id: 多维表格的app_id
            table_id: 多维表格中的table_id
            page_size: 每页记录数，默认100
            
        Returns:
            dict: 多维表格的记录数据
            
        Raises:
            Exception: 获取多维表格数据失败时抛出异常
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
        params = {
            "page_size": page_size
        }
        
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                return result["data"]
            else:
                raise Exception(f"获取多维表格数据失败：{result.get('msg')}")
        else:
            raise Exception(f"获取多维表格数据失败：HTTP {response.status_code} - {response.text}")
    
    def get_wiki_content(self, wiki_id: str) -> dict:
        """
        获取知识库文档内容
        
        Args:
            wiki_id: 知识库文档的wiki_id
            
        Returns:
            dict: 飞书文档API调用结果，包含调试信息
            
        Raises:
            Exception: 获取知识库文档内容失败时抛出异常
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()
        
        # 收集调试信息
        debug_info = {
            "wiki_id": wiki_id,
            "tenant_access_token": self.tenant_access_token,
            "api_calls": []
        }
        
        try:
            # 1. 尝试使用drive/v1/files/get_by_url接口获取文件信息
            print("🔍 尝试使用drive/v1/files/get_by_url接口获取文件信息...")
            drive_url = "https://open.feishu.cn/open-apis/drive/v1/files/get_by_url"
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}",
                "Content-Type": "application/json"
            }
            
            drive_payload = {
                "url": f"https://t0ah9wh5h5f.feishu.cn/wiki/{wiki_id}"
            }
            
            drive_response = requests.post(drive_url, json=drive_payload, headers=headers)
            debug_info["api_calls"].append({
                "url": drive_url,
                "method": "POST",
                "status_code": drive_response.status_code,
                "response": drive_response.text
            })
            
            if drive_response.status_code == 200:
                drive_result = drive_response.json()
                if drive_result.get("code") == 0:
                    debug_info["file_info"] = drive_result["data"]
                    print(f"✅ 成功获取文件信息: {drive_result['data'].get('name', '未知文件名')}")
                    
                    # 获取file_token
                    file_token = drive_result["data"]["file_token"]
                    debug_info["file_token"] = file_token
                    print(f"✅ 获取到file_token: {file_token}")
                    
                    return debug_info
                else:
                    print(f"❌ drive/v1/files/get_by_url接口调用失败: {drive_result.get('msg')}")
            else:
                print(f"❌ drive/v1/files/get_by_url接口HTTP错误: {drive_response.status_code} - {drive_response.text}")
            
            # 2. 尝试直接获取token信息（调试用）
            print("\n🔍 尝试获取token的基本信息...")
            debug_info["token_valid"] = True
            
            return debug_info
            
        except Exception as e:
            print(f"❌ API调用发生异常: {str(e)}")
            debug_info["error"] = str(e)
            return debug_info


def main():
    """
    示例：从sk.md文件获取飞书文档URL并获取文档数据
    """
    # 读取sk.md文件，获取第9行的飞书文档URL
    sk_file_path = "/Users/wangqiao/Downloads/github_project/fastapi-enterprise-framework-template/docs/feishu/sk.md"
    
    try:
        # 读取sk.md文件第9行
        with open(sk_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) >= 9:
                feishu_url = lines[8].strip()  # 索引8对应第9行
                print(f"✅ 从sk.md文件获取的飞书文档URL: {feishu_url}")
            else:
                raise Exception(f"sk.md文件行数不足，无法获取第9行的飞书文档URL")
        
        # 初始化飞书文档API客户端
        feishu_api = FeishuDocAPI()
        
        # 提取file_id
        file_id = feishu_api.extract_file_id_from_url(feishu_url)
        print(f"✅ 从URL提取的file_id: {file_id}")
        
        # 获取文档内容
        print("\n📥 正在获取飞书文档数据...")
        content = feishu_api.get_wiki_content(file_id)
        print(f"✅ 飞书文档数据获取成功！")
        
        # 打印文档内容摘要
        print("\n📋 文档内容摘要：")
        print(f"- 数据类型: {type(content)}")
        print(f"- 包含字段: {list(content.keys())}")
        
        # 保存文档内容到本地文件
        output_file = f"/Users/wangqiao/Downloads/github_project/fastapi-enterprise-framework-template/docs/feishu/output_{file_id}.json"
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 文档内容已保存到本地文件: {output_file}")
        print("\n🎉 飞书文档数据获取任务完成！")
        
    except Exception as e:
        print(f"\n❌ 操作失败: {e}")
        import traceback
        print(f"\n详细错误信息:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
