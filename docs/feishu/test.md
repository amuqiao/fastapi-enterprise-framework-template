通过飞书开放平台API获取文档信息，核心流程包括创建应用获取凭证、获取访问令牌、调用文档API三个步骤。

前期准备：创建应用并配置权限

1.  创建应用
    访问https://open.feishu.cn/app创建“企业自建应用”，填写名称、描述并选择所需能力（如机器人）。

2.  配置权限
    在应用详情页的“权限管理”中，申请以下必要权限：
    ◦ 查看、评论、编辑和管理所有文件（云空间）

    ◦ 查看、评论和导出文档（云文档）

    ◦ 按需添加其他权限（如电子表格操作）。

3.  获取凭证
    在“凭证与基础信息”页获取App ID和App Secret，用于后续获取访问令牌。

获取访问令牌

飞书API需通过令牌鉴权，通常使用tenant_access_token（应用级别权限）：
import requests

def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = requests.post(url, json=payload)
    return response.json().get("tenant_access_token")

# 示例
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"
token = get_tenant_access_token(app_id, app_secret)


获取文档内容与元数据

获取文档列表

列出“我的空间”根目录下的文件：
def list_files(token):
    url = "https://open.feishu.cn/open-apis/drive/v1/files"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"direction": "DESC", "order_by": "EditedTime"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

files = list_files(token)
for file in files["data"]["files"]:
    print(f"名称: {file['name']}, 类型: {file['type']}, Token: {file['token']}")


获取文档内容

根据文档类型选择API：

•   新版文档（docx）：使用/docs/v1/content接口
    def get_docx_content(token, doc_token):
        url = "https://open.feishu.cn/open-apis/docs/v1/content"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"doc_token": doc_token, "doc_type": "docx", "content_type": "markdown"}
        response = requests.get(url, headers=headers, params=params)
        return response.json().get("data", {}).get("content", "")

    content = get_docx_content(token, "DOC_TOKEN")
    print(content)
    

•   旧版文档（doc）：使用/doc/v2/{docToken}/content接口
    def get_doc_content(token, doc_token):
        url = f"https://open.feishu.cn/open-apis/doc/v2/{doc_token}/content"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        return response.json().get("data", {}).get("content", "")
    

获取块级内容（结构化数据）

适用于解析文档结构（如段落、标题、表格）：
def get_document_blocks(token, document_id):
    url = f"https://open.feishu.cn/open-apis/docs/docx/v1/documents/{document_id}/blocks"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("data", {}).get("items", [])

blocks = get_document_blocks(token, "DOCUMENT_ID")
for block in blocks:
    print(f"块类型: {block['block_type']}, 内容: {block.get('text', '')}")


实战案例：自动同步飞书文档到微信群

以下是一个简化版的自动化流程，用于读取飞书文档并通过微信机器人推送内容：

1.  获取文档块内容：使用get_document_blocks提取文本、标题等块。
2.  处理图片：若块中包含图片（block_type为图片），需调用媒体API获取临时下载链接。
3.  格式化内容：拼接文本块，按换行符分割消息，图片单独发送。
4.  通过微信机器人API发送。

注意事项

•   权限问题：确保应用已获授权，且文档已共享给应用（可通过文档右上角“···”→“添加应用”配置）。

•   令牌有效期：tenant_access_token有效期通常为2小时，需定期刷新。

•   错误处理：常见错误码包括91403（无权限）、91402（文档不存在），需根据返回码排查。

•   速率限制：API调用有QPS限制（如获取文件列表为5次/秒），需合理设计重试机制。

通过以上步骤，您可以高效集成飞书文档API，实现内容自动化处理。如需进一步探索，可参考飞书官方文档中的https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list。