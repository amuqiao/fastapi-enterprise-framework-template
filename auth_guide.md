# 登录注册与认证使用说明

## 系统概述

本系统基于FastAPI框架实现，提供了完整的用户注册、登录和JWT认证功能。通过该系统，您可以：
- 创建新用户账号
- 使用账号登录获取访问令牌
- 使用访问令牌访问受保护的API资源

## 技术栈

- **框架**：FastAPI
- **认证方式**：JWT (JSON Web Token)
- **令牌类型**：Bearer Token
- **令牌有效期**：30分钟
- **API文档**：Swagger UI (http://localhost:8001/docs)

## API端点说明

### 1. 用户注册

**端点**：`POST /api/v1/auth/register`

**功能**：创建新用户账号

**请求体**：
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**参数说明**：
- `username`：用户名，必填，唯一
- `email`：邮箱地址，必填，唯一
- `password`：密码，必填，建议长度不少于6位

**响应示例**：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "id": 1,
  "created_at": "2025-12-20T07:00:00",
  "updated_at": "2025-12-20T07:00:00"
}
```

### 2. 用户登录

**端点**：`POST /api/v1/auth/login`

**功能**：使用用户名和密码登录，获取访问令牌

**请求体**（表单形式）：
```
username=testuser&password=testpassword
```

**参数说明**：
- `username`：用户名，必填
- `password`：密码，必填

**响应示例**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. 获取当前用户信息

**端点**：`GET /api/v1/users/me`

**功能**：获取当前登录用户的详细信息

**认证要求**：需要有效JWT令牌

**响应示例**：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "id": 1,
  "created_at": "2025-12-20T07:00:00",
  "updated_at": "2025-12-20T07:00:00"
}
```

### 4. 获取指定用户信息

**端点**：`GET /api/v1/users/{user_id}`

**功能**：根据用户ID获取用户信息

**认证要求**：需要有效JWT令牌

**参数说明**：
- `user_id`：用户ID，必填

**响应示例**：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "id": 1,
  "created_at": "2025-12-20T07:00:00",
  "updated_at": "2025-12-20T07:00:00"
}
```

## 认证机制

### JWT令牌结构

JWT令牌由三部分组成：
- **Header**：包含令牌类型和签名算法
- **Payload**：包含用户信息和过期时间
- **Signature**：用于验证令牌的完整性

### 令牌使用方法

1. 从登录接口获取访问令牌
2. 在请求头中添加`Authorization`字段
3. 字段值格式：`Bearer <your_access_token>`
4. 发送请求到受保护的API端点

### 令牌有效期

- 访问令牌默认有效期为30分钟
- 过期后需要重新登录获取新令牌
- 建议在客户端实现令牌自动刷新机制

## 使用示例

### 1. 使用curl命令

#### 注册新用户

```bash
curl -X POST "http://localhost:8001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpassword"}'
```

#### 用户登录

```bash
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword"
```

#### 使用令牌访问受保护资源

```bash
curl -X GET "http://localhost:8001/api/v1/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. 使用Python requests库

```python
import requests

# 注册新用户
register_url = "http://localhost:8001/api/v1/auth/register"
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword"
}
response = requests.post(register_url, json=register_data)
print("注册响应:", response.json())

# 用户登录
login_url = "http://localhost:8001/api/v1/auth/login"
login_data = {
    "username": "testuser",
    "password": "testpassword"
}
response = requests.post(login_url, data=login_data)
login_response = response.json()
print("登录响应:", login_response)

# 获取访问令牌
token = login_response["access_token"]
auth_header = {"Authorization": f"Bearer {token}"}

# 访问受保护资源
protected_url = "http://localhost:8001/api/v1/users/me"
response = requests.get(protected_url, headers=auth_header)
print("受保护资源响应:", response.json())
```

### 3. 使用Swagger UI

#### 注册新用户

1. 打开Swagger UI：http://localhost:8001/docs
2. 找到`POST /api/v1/auth/register`端点
3. 点击"Try it out"按钮
4. 在请求体中填写用户信息
5. 点击"Execute"按钮
6. 查看响应结果

#### 用户登录

1. 找到`POST /api/v1/auth/login`端点
2. 点击"Try it out"按钮
3. 填写用户名和密码
4. 点击"Execute"按钮
5. 从响应中获取`access_token`

#### 授权Swagger UI

1. 点击页面顶部的"Authorize"按钮
2. 在"Value"字段中输入`Bearer <your_access_token>`
3. 点击"Authorize"按钮完成授权
4. 点击"Close"按钮关闭对话框

#### 访问受保护资源

1. 找到`GET /api/v1/users/me`端点
2. 点击"Try it out"按钮
3. 点击"Execute"按钮
4. 查看响应结果

## 常见问题解答

### 1. 注册失败，提示用户名或邮箱已存在

**解决方法**：使用不同的用户名和邮箱地址重新注册。

### 2. 登录失败，提示"Incorrect username or password"

**解决方法**：检查用户名和密码是否正确，确保没有大小写错误。

### 3. 访问受保护资源时提示"401 Unauthorized"

**解决方法**：
- 检查令牌是否正确，确保包含"Bearer "前缀
- 检查令牌是否过期，过期后需要重新登录
- 检查令牌是否被篡改

### 4. 令牌过期了怎么办

**解决方法**：重新调用登录接口获取新的访问令牌。

### 5. 如何在前端应用中管理令牌

**建议**：
- 将令牌存储在安全的地方（如localStorage或sessionStorage）
- 在请求拦截器中自动添加Authorization头
- 实现令牌过期自动刷新机制
- 登出时清除令牌

## 安全建议

1. **密码安全**：
   - 使用强密码，包含字母、数字和特殊字符
   - 定期更换密码
   - 不要在多个平台使用相同密码

2. **令牌安全**：
   - 不要在公共环境中泄露令牌
   - 不要将令牌存储在明文文件中
   - 定期更换令牌

3. **请求安全**：
   - 生产环境中使用HTTPS协议
   - 不要在URL中传递敏感信息
   - 验证请求来源

## 系统配置

### 修改令牌有效期

在`app/core/config.py`文件中修改以下配置：

```python
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 修改为所需分钟数
```

### 修改JWT密钥

在`app/core/config.py`文件中修改以下配置：

```python
SECRET_KEY: str = "your-secret-key"  # 修改为强密钥
```

## 联系方式

如有任何问题或建议，请联系系统管理员。

---

**文档版本**：v1.0  
**更新日期**：2025-12-20  
**适用系统**：FastAPI Enterprise Architecture
