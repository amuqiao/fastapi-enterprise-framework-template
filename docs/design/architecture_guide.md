# FastAPI 企业级架构设计指南

## 一、项目概述

这是一个基于FastAPI框架的生产级架构设计，旨在作为多个项目的通用轮子项目。该架构支持多环境部署、API版本控制、模块化设计和企业级特性，适合构建各种规模的FastAPI应用。架构设计遵循高内聚、低耦合原则，确保未来新增功能时基础架构无需变更，具备良好的可扩展性和可维护性。

## 二、设计原则与理念

### 1. 架构设计原则

- ✅ **分层设计**：明确的职责划分，各层之间通过接口通信
- ✅ **模块化设计**：按业务域划分模块，支持独立开发和部署
- ✅ **依赖倒置**：高层模块不依赖低层模块，两者都依赖抽象接口
- ✅ **单一职责**：每个模块、类和函数只负责一个明确的功能
- ✅ **接口抽象**：通过接口定义契约，实现模块间解耦
- ✅ **可测试性**：设计便于单元测试和集成测试的架构
- ✅ **可扩展性**：支持新功能的无缝添加，无需修改现有架构
- ✅ **类型安全**：使用Pydantic进行数据验证，确保类型安全

### 2. DDD领域驱动设计

本架构采用DDD领域驱动设计思想，将业务逻辑与技术实现分离：

- **领域模型**：核心业务概念的抽象，包含实体(Entity)、值对象(Value Object)和聚合根(Aggregate Root)
- **领域服务**：封装跨实体的业务逻辑
- **领域事件**：用于处理领域内的异步通信
- **仓储**：负责领域对象的持久化和检索

### 3. 模块化设计思想

- **业务模块化**：按业务域划分模块，如用户模块、订单模块等
- **技术模块化**：按技术功能划分模块，如配置模块、日志模块等
- **插件化设计**：支持通过插件机制扩展功能，无需修改核心代码

## 三、整体架构设计

### 1. 整体架构图

```mermaid
graph TD
    subgraph 客户端层
        A[Web客户端] --> B[API网关]
        C[移动客户端] --> B
        D[第三方服务] --> B
    end
    
    subgraph 应用层
        B --> E[FastAPI应用]
        
        subgraph 核心框架层
            E --> F[路由模块]
            E --> G[中间件模块]
            E --> H[依赖注入模块]
            E --> I[配置管理模块]
        end
        
        subgraph 业务逻辑层
            F --> J[服务层]
            J --> K[仓储层]
            J --> L[领域事件]
        end
        
        subgraph 基础设施层
            K --> M[数据库]
            J --> N[缓存层]
            L --> O[消息队列]
            E --> P[日志模块]
            E --> Q[安全模块]
            E --> R[观测性模块]
        end
        
        subgraph 扩展层
            E --> S[插件架构]
        end
    end
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style C fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style D fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style F fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style G fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style I fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style J fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style K fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style L fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style M fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style N fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style O fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style P fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style Q fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style R fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style S fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
```

### 2. 分层设计

| 层级 | 职责 | 核心模块 |
| --- | --- | --- |
| **核心框架层** | 提供基础框架支持 | 路由模块、中间件模块、依赖注入模块、配置管理模块 |
| **业务逻辑层** | 封装核心业务逻辑 | 服务层、仓储层、领域事件 |
| **基础设施层** | 提供技术支持 | 数据库、缓存层、消息队列、日志模块、安全模块、观测性模块 |
| **扩展层** | 支持架构扩展 | 插件架构 |

### 3. 模块功能架构图

```mermaid
graph TD
    subgraph 核心框架模块
        A[配置管理] --> B[依赖注入]
        C[路由与API版本控制] --> D[中间件]
        B --> D
    end
    
    subgraph 业务逻辑模块
        E[服务层] --> F[仓储层]
        E --> G[领域事件]
    end
    
    subgraph 基础设施模块
        H[安全模块] --> I[观测性模块]
        J[数据库] --> K[缓存层]
        L[消息队列] --> M[异步任务]
    end
    
    subgraph 扩展模块
        N[插件架构] --> O[插件管理器]
    end
    
    coreFrame[核心框架模块] --> busiLogic[业务逻辑模块]
    coreFrame --> infra[基础设施模块]
    busiLogic --> infra
    coreFrame --> ext[扩展模块]
    
    style coreFrame fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style busiLogic fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style infra fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style ext fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style F fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style G fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style H fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style I fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style J fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style K fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style L fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style M fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style N fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style O fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
```

## 四、核心模块设计

### 1. 配置管理模块

**核心作用**：统一管理多环境配置，支持动态配置更新，避免硬编码

**设计特点**：
- 使用Pydantic Settings进行类型安全的配置管理
- 支持多环境配置文件（.env.dev, .env.test, .env.prod）
- 支持环境变量覆盖配置文件
- 配置热更新支持
- 配置验证机制

**模块架构图**：
```mermaid
graph TD
    A[环境变量文件] --> B[Pydantic Settings]
    C[环境变量] --> B
    B --> D[配置验证]
    D --> E[配置实例]
    E --> F[应用使用]
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant EnvFile as 环境变量文件
    participant EnvVar as 环境变量
    participant Pydantic as Pydantic Settings
    participant Validation as 配置验证
    participant Config as 配置实例
    participant App as 应用
    
    EnvFile->>Pydantic: 加载配置文件
    EnvVar->>Pydantic: 读取环境变量
    Pydantic->>Validation: 验证配置
    Validation->>Config: 生成配置实例
    Config->>App: 应用使用配置
    App->>Config: 获取配置值
```

**关键实现**：
```python
# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class DatabaseSettings(BaseSettings):
    """数据库配置"""
    url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20

class RedisSettings(BaseSettings):
    """Redis配置"""
    url: str
    db: int = 0

class SecuritySettings(BaseSettings):
    """安全配置"""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

class AppSettings(BaseSettings):
    """应用配置"""
    name: str = "FastAPI Enterprise"
    version: str = "1.0.0"
    debug: bool = False
    
    # 子配置
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

# 全局配置实例
settings = AppSettings()
```

### 2. 依赖注入模块

**核心作用**：封装通用依赖，实现依赖注入，提高代码复用性和可测试性

**设计特点**：
- 基于FastAPI的依赖注入系统
- 支持作用域管理（请求级、应用级）
- 依赖自动注入
- 支持依赖替换，便于测试

**模块架构图**：
```mermaid
graph TD
    A[路由函数] --> B[依赖声明]
    B --> C[依赖解析器]
    C --> D{依赖有子依赖?}
    D -->|是| E[递归解析子依赖]
    D -->|否| F[创建依赖实例]
    E --> F
    F --> G[缓存依赖实例]
    G --> H[使用依赖]
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant Router as 路由函数
    participant DepDeclare as 依赖声明
    participant DepResolver as 依赖解析器
    participant SubDep as 子依赖
    participant DepInstance as 依赖实例
    participant AppLogic as 应用逻辑
    
    Router->>DepDeclare: 声明依赖
    DepDeclare->>DepResolver: 请求解析依赖
    DepResolver->>SubDep: 检查是否有子依赖
    SubDep->>DepResolver: 返回子依赖实例
    DepResolver->>DepInstance: 创建依赖实例
    DepInstance->>AppLogic: 传递给应用逻辑
    AppLogic->>Router: 执行路由逻辑
```

**关键实现**：
```python
# app/dependencies/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import async_session_maker

async def get_db_session() -> AsyncSession:
    """获取数据库会话"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 3. 路由与API版本控制

**核心作用**：处理HTTP请求，支持API版本控制，实现路由与业务逻辑分离

**设计特点**：
- 支持URL路径版本控制
- 支持Header版本控制
- 路由自动注册
- 支持路由分组

**模块架构图**：
```mermaid
graph TD
    A[主API路由器] --> B[版本路由v1]
    A --> C[版本路由v2]
    B --> D[资源路由1]
    B --> E[资源路由2]
    C --> F[资源路由1]
    C --> G[资源路由2]
    D --> H[路径参数处理]
    E --> I[查询参数处理]
    F --> J[路径参数处理]
    G --> K[查询参数处理]
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style G fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style I fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style J fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style K fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant APIRouter as 主API路由器
    participant VersionRouter as 版本路由
    participant ResourceRouter as 资源路由
    participant PathHandler as 路径参数处理
    participant QueryHandler as 查询参数处理
    participant Service as 服务层
    
    Client->>APIRouter: 发送请求
    APIRouter->>VersionRouter: 路由到版本
    VersionRouter->>ResourceRouter: 路由到资源
    ResourceRouter->>PathHandler: 处理路径参数
    ResourceRouter->>QueryHandler: 处理查询参数
    PathHandler->>Service: 传递参数
    QueryHandler->>Service: 传递参数
    Service->>Client: 返回响应
```

**关键实现**：
```python
# app/api/__init__.py
from fastapi import APIRouter
from app.api.v1 import api_router as v1_router
from app.api.v2 import api_router as v2_router

# 主API路由器
api_router = APIRouter(prefix="/api")

# 注册版本路由
api_router.include_router(v1_router, prefix="/v1", tags=["v1"])
api_router.include_router(v2_router, prefix="/v2", tags=["v2"])
```

### 4. 服务层设计（DDD增强）

**核心作用**：封装核心业务逻辑，实现业务与技术分离，是连接表示层（API路由）和数据访问层（仓储层）的桥梁。

**设计理念**：
- **业务逻辑封装**：将复杂的业务规则和流程封装在服务层，避免业务逻辑分散到控制器或数据访问层
- **DDD领域驱动**：基于领域模型设计，实现领域服务、领域事件和领域规则
- **接口抽象**：通过抽象接口定义服务契约，实现依赖倒置，便于测试和替换实现
- **事务管理**：负责业务事务的管理，确保数据一致性

**模块架构图**：
```mermaid
graph TD
    subgraph 服务层架构
        A[BaseService基类] --> B[UserService用户服务]
        A --> C[OrderService订单服务]
        A --> D[ProductService商品服务]
        
        B --> E[业务规则验证]
        B --> F[领域事件发布]
        B --> G[日志记录]
        
        C --> E
        C --> F
        C --> G
        
        D --> E
        D --> F
        D --> G
        
        B --> H[UserRepository用户仓储]
        C --> I[OrderRepository订单仓储]
        D --> J[ProductRepository商品仓储]
    end
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style I fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style J fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant API as API路由层
    participant Service as 服务层
    participant Repo as 仓储层
    participant DB as 数据库
    participant Event as 领域事件
    participant Logger as 日志模块
    
    API->>Service: 调用服务方法
    Service->>Service: 业务规则验证
    Service->>Repo: 调用仓储方法
    Repo->>DB: 执行数据库操作
    DB-->>Repo: 返回数据
    Repo-->>Service: 返回结果
    Service->>Event: 发布领域事件
    Service->>Logger: 记录日志
    Service-->>API: 返回响应
```

**服务层与仓储层的关系**：
- 服务层调用仓储层来获取和持久化数据
- 仓储层只负责数据访问，不包含业务逻辑
- 服务层负责业务规则验证、业务流程控制和领域事件发布

**领域服务目录结构设计**：

服务层采用DDD领域驱动设计，按业务域组织服务代码，每个业务域拥有自己的服务实现。以下是用户域和订单域的服务目录结构示例：

```
app/domains/
├── user/                # 用户领域
│   └── services/        # 用户领域服务
│       ├── __init__.py
│       └── user_service.py   # 用户服务实现
└── order/               # 订单领域
    └── services/        # 订单领域服务
        ├── __init__.py
        └── order_service.py  # 订单服务实现
```

**基类设计的作用与优势**：

服务层基类`BaseService`的设计具有以下重要作用：

1. **统一接口规范**：定义了服务层必须实现的核心方法，确保所有服务类遵循相同的接口规范
2. **减少重复代码**：封装了通用的服务逻辑，避免每个服务类重复实现相同的方法
3. **提高可维护性**：统一的接口设计使代码更易于理解和维护
4. **支持泛型**：使用泛型设计，支持不同类型的实体操作
5. **便于扩展**：新增领域服务时，只需继承基类并实现抽象方法，无需修改基类
6. **便于测试**：统一的接口设计使单元测试更加方便

**为什么新增领域服务不需要修改基类？**

- 基类采用抽象类设计，定义了通用的服务接口
- 新增领域服务时，只需继承基类并实现抽象方法
- 基类的设计遵循开闭原则（对扩展开放，对修改关闭）
- 每个领域服务可以根据自身需求扩展额外的方法，而不影响基类

**关键实现**：
```python
# app/services/base.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class BaseService(ABC, Generic[T]):
    """服务层基类，定义通用的服务接口"""
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """根据ID获取实体"""
        pass
    
    @abstractmethod
    async def create(self, obj: T) -> T:
        """创建实体"""
        pass
    
    @abstractmethod
    async def update(self, id: int, obj: T) -> Optional[T]:
        """更新实体"""
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """删除实体"""
        pass
```

**用户服务示例**：
```python
# app/domains/user/services/user_service.py
from app.services.base import BaseService
from app.domains.user.models import User
from app.domains.user.schemas import UserCreate, UserUpdate
from app.domains.user.repositories.user_repository import UserRepository
from app.observability.logging import logger
from app.infrastructure.queue.connection import get_queue_producer

class UserService(BaseService[User]):
    """用户服务，继承自BaseService"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def get_by_id(self, id: int) -> Optional[User]:
        """根据ID获取用户"""
        return await self.user_repository.get_by_id(id)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户，扩展方法"""
        return await self.user_repository.get_by_email(email)
    
    async def create(self, user_create: UserCreate) -> User:
        """创建用户"""
        # 业务规则验证
        existing_user = await self.get_by_email(user_create.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # 创建用户
        user = await self.user_repository.create(user_create)
        
        # 发布领域事件
        async with get_queue_producer() as producer:
            await producer.publish("user.created", {"user_id": user.id, "email": user.email})
        
        logger.info(f"User created: {user.id}")
        return user
    
    async def update(self, id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户"""
        user = await self.get_by_id(id)
        if not user:
            return None
        
        # 更新用户
        updated_user = await self.user_repository.update(user, user_update)
        
        # 发布领域事件
        async with get_queue_producer() as producer:
            await producer.publish("user.updated", {"user_id": updated_user.id})
        
        logger.info(f"User updated: {updated_user.id}")
        return updated_user
    
    async def delete(self, id: int) -> bool:
        """删除用户"""
        user = await self.get_by_id(id)
        if not user:
            return False
        
        # 删除用户
        await self.user_repository.delete(user)
        
        # 发布领域事件
        async with get_queue_producer() as producer:
            await producer.publish("user.deleted", {"user_id": id})
        
        logger.info(f"User deleted: {id}")
        return True
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """用户认证，扩展方法"""
        user = await self.get_by_email(email)
        if not user:
            return None
        
        # 密码验证
        if not user.verify_password(password):
            return None
        
        logger.info(f"User authenticated: {user.id}")
        return user
```

**订单服务示例**：
```python
# app/domains/order/services/order_service.py
from app.services.base import BaseService
from app.domains.order.models import Order
from app.domains.order.schemas import OrderCreate, OrderUpdate
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.user.services.user_service import UserService
from app.observability.logging import logger
from app.infrastructure.queue.connection import get_queue_producer

class OrderService(BaseService[Order]):
    """订单服务，继承自BaseService"""
    
    def __init__(self, order_repository: OrderRepository, user_service: UserService):
        self.order_repository = order_repository
        self.user_service = user_service
    
    async def get_by_id(self, id: int) -> Optional[Order]:
        """根据ID获取订单"""
        return await self.order_repository.get_by_id(id)
    
    async def create(self, order_create: OrderCreate) -> Order:
        """创建订单"""
        # 验证用户是否存在
        user = await self.user_service.get_by_id(order_create.user_id)
        if not user:
            raise ValueError("User not found")
        
        # 创建订单
        order = await self.order_repository.create(order_create)
        
        # 发布领域事件
        async with get_queue_producer() as producer:
            await producer.publish("order.created", {"order_id": order.id, "user_id": order.user_id})
        
        logger.info(f"Order created: {order.id}")
        return order
    
    async def update(self, id: int, order_update: OrderUpdate) -> Optional[Order]:
        """更新订单"""
        order = await self.get_by_id(id)
        if not order:
            return None
        
        # 更新订单
        updated_order = await self.order_repository.update(order, order_update)
        
        # 发布领域事件
        async with get_queue_producer() as producer:
            await producer.publish("order.updated", {"order_id": updated_order.id})
        
        logger.info(f"Order updated: {updated_order.id}")
        return updated_order
    
    async def delete(self, id: int) -> bool:
        """删除订单"""
        order = await self.get_by_id(id)
        if not order:
            return False
        
        # 删除订单
        await self.order_repository.delete(order)
        
        # 发布领域事件
        async with get_queue_producer() as producer:
            await producer.publish("order.deleted", {"order_id": id})
        
        logger.info(f"Order deleted: {id}")
        return True
    
    async def get_orders_by_user_id(self, user_id: int) -> list[Order]:
        """根据用户ID获取订单，扩展方法"""
        return await self.order_repository.get_orders_by_user_id(user_id)
```

### 5. 仓储层设计（接口抽象）

**核心作用**：抽象数据访问层，负责领域对象的持久化和检索，实现数据访问与业务逻辑分离。

**设计理念**：
- **接口抽象**：通过接口定义数据访问契约，实现依赖倒置，便于测试和替换实现
- **多数据库支持**：支持多种数据库后端（SQLAlchemy, MongoDB等）
- **事务支持**：参与服务层的事务管理，确保数据一致性
- **查询构建器**：支持灵活的查询构建，满足复杂查询需求

**模块架构图**：
```mermaid
graph TD
    subgraph 仓储层架构
        A[BaseRepository基类] --> B[UserRepository用户仓储]
        A --> C[OrderRepository订单仓储]
        A --> D[ProductRepository商品仓储]
        
        B --> E[数据库会话]
        C --> E
        D --> E
        
        E --> F[SQLAlchemy ORM]
        E --> G[异步操作]
        
        F --> H[查询构建器]
        F --> I[事务管理]
    end
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style I fill:#FF6B6B,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant Service as 服务层
    participant Repo as 仓储层
    participant Session as 数据库会话
    participant ORM as SQLAlchemy ORM
    participant DB as 数据库
    
    Service->>Repo: 调用仓储方法
    Repo->>Session: 使用数据库会话
    Session->>ORM: 构建SQL查询
    ORM->>DB: 执行数据库操作
    DB-->>ORM: 返回查询结果
    ORM-->>Session: 转换为对象
    Session-->>Repo: 返回实体对象
    Repo-->>Service: 返回处理结果
```

**仓储层与服务层的关系**：
- 仓储层是服务层的依赖，服务层通过仓储层访问数据
- 仓储层只负责数据访问，不包含业务规则
- 仓储层的方法设计应该与业务需求紧密相关，而不是简单的CRUD操作

**关键实现**：
```python
# app/repositories/base.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """仓储层基类"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """根据ID获取实体"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """获取所有实体"""
        pass
    
    @abstractmethod
    async def create(self, obj: T) -> T:
        """创建实体"""
        pass
    
    @abstractmethod
    async def update(self, obj: T, update_data: dict) -> T:
        """更新实体"""
        pass
    
    @abstractmethod
    async def delete(self, obj: T) -> None:
        """删除实体"""
        pass
```

**用户仓储示例**：
```python
# app/domains/user/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.domains.user.models import User
from app.domains.user.schemas import UserCreate, UserUpdate

class UserRepository(BaseRepository[User]):
    """用户仓储"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
    
    async def get_by_id(self, id: int) -> Optional[User]:
        """根据ID获取用户"""
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取所有用户"""
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, user_create: UserCreate) -> User:
        """创建用户"""
        user = User(**user_create.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(self, user: User, user_update: UserUpdate) -> User:
        """更新用户"""
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        """删除用户"""
        await self.session.delete(user)
        await self.session.commit()
    
    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """根据角色获取用户"""
        stmt = select(User).where(User.role == role).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
```

### 6. 中间件模块

**核心作用**：处理请求/响应生命周期的横切逻辑

**设计特点**：
- 支持多种中间件
- 中间件顺序可控
- 支持自定义中间件
- 内置常用中间件（CORS、限流、日志、认证等）

**模块架构图**：
```mermaid
graph TD
    subgraph 中间件链
        A[CORS中间件] --> B[日志中间件]
        B --> C[安全中间件]
        C --> D[限流中间件]
        D --> E[自定义中间件]
    end
    
    subgraph 中间件管理
        F[中间件注册器] --> A
        F --> B
        F --> C
        F --> D
        F --> E
    end
    
    Client[客户端请求] --> 中间件链
    中间件链 --> Router[路由处理]
    Router --> 中间件链
    中间件链 --> Client
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style Client fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style Router fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style 中间件链 fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style 中间件管理 fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant CORS as CORS中间件
    participant Logging as 日志中间件
    participant Security as 安全中间件
    participant RateLimit as 限流中间件
    participant Router as 路由层
    
    Client->>CORS: 请求经过CORS中间件
    CORS->>Logging: 请求经过日志中间件
    Logging->>Security: 请求经过安全中间件
    Security->>RateLimit: 请求经过限流中间件
    RateLimit->>Router: 请求到达路由层
    Router->>RateLimit: 响应返回限流中间件
    RateLimit->>Security: 响应返回安全中间件
    Security->>Logging: 响应返回日志中间件
    Logging->>CORS: 响应返回CORS中间件
    CORS->>Client: 响应返回客户端
```

**关键实现**：
```python
# app/middleware/__init__.py
from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.middleware.logging import add_logging_middleware
from app.middleware.security import add_security_middleware
from app.middleware.rate_limiter import add_rate_limiter_middleware

def register_middlewares(app: FastAPI) -> None:
    """注册所有中间件"""
    add_cors_middleware(app)
    add_logging_middleware(app)
    add_security_middleware(app)
    add_rate_limiter_middleware(app)
```

### 7. 安全模块

**核心作用**：提供全面的安全保障

**设计特点**：
- 支持多种认证方式（JWT、API Key、OAuth2等）
- 细粒度权限控制
- 输入验证和输出过滤
- 防止常见安全漏洞（SQL注入、XSS、CSRF等）

**模块架构图**：
```mermaid
graph TD
    subgraph 安全模块
        A[认证模块] --> B[JWT认证]
        A --> C[API Key认证]
        A --> D[OAuth2认证]
        
        E[授权模块] --> F[基于角色的访问控制]
        E --> G[基于权限的访问控制]
        
        H[数据安全] --> I[输入验证]
        H --> J[输出过滤]
        H --> K[加密解密]
        
        L[安全防护] --> M[防止SQL注入]
        L --> N[防止XSS攻击]
        L --> O[防止CSRF攻击]
    end
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style I fill:#FF6B6B,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style J fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style K fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style L fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style M fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style N fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style O fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant Client as 客户端
    participant Router as 路由层
    participant Auth as 认证模块
    participant JWT as JWT处理
    participant Settings as 配置
    participant DB as 数据库
    participant Authz as 授权模块
    
    Client->>Router: 发送请求（带Token）
    Router->>Auth: 调用get_current_user
    Auth->>JWT: 解析Token
    JWT->>Settings: 获取密钥
    JWT->>Auth: 返回用户标识
    Auth->>DB: 查询用户信息
    DB->>Auth: 返回用户数据
    Auth->>Authz: 检查权限
    Authz->>Router: 授权结果
    Router->>Client: 返回响应
```

**关键实现**：
```python
# app/security/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # 从数据库获取用户
    # user = await user_repository.get_by_username(username)
    # if user is None:
    #     raise credentials_exception
    return username
```

### 8. 观测性模块

**核心作用**：提供全面的监控、追踪和日志功能，便于系统的运维、调试和性能优化

**设计特点**：
- 结构化日志：支持JSON格式日志，便于分析和监控
- 请求追踪：支持分布式追踪，便于定位请求瓶颈
- 性能监控：支持指标收集，便于性能分析和优化
- 健康检查：支持系统健康状态检查
- 可扩展性：支持多种观测性工具集成

**模块架构图**：
```mermaid
graph TD
    subgraph 观测性模块
        A[日志模块] --> B[结构化日志]
        A --> C[控制台输出]
        A --> D[文件输出]
        A --> E[日志级别控制]
        
        F[监控模块] --> G[指标收集]
        F --> H[健康检查]
        F --> I[性能监控]
        
        J[追踪模块] --> K[分布式追踪]
        J --> L[请求追踪]
        J --> M[链路可视化]
    end
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style I fill:#FF6B6B,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style J fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style K fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style L fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style M fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant App as 应用代码
    participant Logger as 日志模块
    participant Config as 日志配置
    participant Console as 控制台
    participant File as 日志文件
    participant Monitor as 监控模块
    participant Metrics as 指标收集
    participant Health as 健康检查
    
    App->>Logger: 记录日志
    Logger->>Config: 获取日志配置
    Logger->>Console: 输出到控制台
    Logger->>File: 写入日志文件
    
    App->>Monitor: 收集指标
    Monitor->>Metrics: 处理指标数据
    Monitor->>Health: 执行健康检查
    Health->>Monitor: 返回健康状态
    Monitor->>Metrics: 暴露指标端点
```

**日志配置说明**：
- 日志配置统一在观测性模块中管理
- 支持多环境日志配置
- 支持控制台和文件两种日志输出方式
- 支持不同日志级别配置
- 支持结构化日志格式

**关键实现**：
```python
# app/observability/logging.py
import logging
from logging.config import dictConfig
from app.config.settings import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(extra)s",
        },
        "console": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": "DEBUG" if settings.debug else "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 100,  # 100MB
            "backupCount": 5,
            "formatter": "json",
            "level": "INFO",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if settings.debug else "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# 配置日志
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")
```

**使用示例**：
```python
# 在代码中使用日志
from app.observability.logging import logger

logger.info("User created", extra={"user_id": 1, "email": "test@example.com"})
logger.error("Failed to create user", exc_info=True, extra={"email": "test@example.com"})
```

### 9. 异步任务与消息队列

**核心作用**：处理异步任务，支持事件驱动架构，提高系统的并发性能和可靠性

**设计特点**：
- 支持多种消息队列集成（RabbitMQ, Redis, Kafka等）
- 异步任务处理，提高系统并发性能
- 事件驱动设计，支持松耦合架构
- 任务重试机制，提高系统可靠性
- 统一的消息队列接口，便于切换实现

**模块架构图**：
```mermaid
graph TD
    subgraph 消息队列模块
        A[消息队列抽象接口] --> B[RabbitMQ实现]
        A --> C[Redis实现]
        A --> D[Kafka实现]
        
        E[连接管理] --> B
        E --> C
        E --> D
        
        F[生产者] --> B
        F --> C
        F --> D
        
        G[消费者] --> B
        G --> C
        G --> D
    end
    
    subgraph 异步任务模块
        H[任务基类] --> I[邮件发送任务]
        H --> J[数据处理任务]
        H --> K[通知任务]
        
        L[任务调度] --> I
        L --> J
        L --> K
    end
    
    subgraph 事件驱动架构
        M[领域事件] --> F
        G --> L
    end
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style I fill:#FF6B6B,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style J fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style K fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style L fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style M fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant Service as 服务层
    participant Event as 领域事件
    participant Producer as 消息生产者
    participant MQ as 消息队列
    participant Consumer as 消息消费者
    participant Task as 异步任务
    participant External as 外部系统
    
    Service->>Event: 触发领域事件
    Event->>Producer: 发布消息
    Producer->>MQ: 发送到消息队列
    MQ->>Consumer: 推送消息
    Consumer->>Task: 执行异步任务
    Task->>External: 调用外部系统
    External->>Task: 返回结果
    Task->>Consumer: 完成任务
```

**消息队列选型建议**：
| 消息队列 | 适用场景 | 特点 |
| --- | --- | --- |
| **RabbitMQ** | 异步任务处理、事件驱动、工作队列 | 可靠性高、支持多种协议、成熟稳定 |
| **Redis** | 简单异步任务、缓存、实时数据处理 | 性能高、部署简单、支持多种数据结构 |
| **Kafka** | 大规模数据流处理、日志收集、实时分析 | 高吞吐量、支持持久化、分布式设计 |

**目录结构设计**：
```
app/infrastructure/queue/
├── __init__.py
├── base.py              # 消息队列抽象接口
├── connection.py        # 连接管理
├── producers/           # 消息生产者
│   ├── __init__.py
│   ├── rabbitmq_producer.py
│   ├── redis_producer.py
│   └── kafka_producer.py
├── consumers/           # 消息消费者
│   ├── __init__.py
│   ├── rabbitmq_consumer.py
│   ├── redis_consumer.py
│   └── kafka_consumer.py
└── config.py            # 消息队列配置
```

**关键实现**：
```python
# app/infrastructure/queue/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseQueue(ABC):
    """消息队列抽象基类"""
    
    @abstractmethod
    async def connect(self) -> None:
        """连接到消息队列"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """断开消息队列连接"""
        pass
    
    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """发布消息"""
        pass
    
    @abstractmethod
    async def subscribe(self, topic: str, callback) -> None:
        """订阅消息"""
        pass

# app/infrastructure/queue/connection.py
from app.config.settings import settings
from app.infrastructure.queue.producers.rabbitmq_producer import RabbitMQProducer
from app.infrastructure.queue.producers.redis_producer import RedisProducer
from app.infrastructure.queue.producers.kafka_producer import KafkaProducer

async def get_queue_producer():
    """获取消息队列生产者"""
    queue_type = settings.queue.type  # 从配置中获取消息队列类型
    
    if queue_type == "rabbitmq":
        producer = RabbitMQProducer()
    elif queue_type == "redis":
        producer = RedisProducer()
    elif queue_type == "kafka":
        producer = KafkaProducer()
    else:
        raise ValueError(f"Unsupported queue type: {queue_type}")
    
    await producer.connect()
    try:
        yield producer
    finally:
        await producer.disconnect()

# app/tasks/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTask(ABC):
    """任务基类"""
    
    @abstractmethod
    async def execute(self, **kwargs: Dict[str, Any]) -> Any:
        """执行任务"""
        pass

# app/tasks/email.py
from app.tasks.base import BaseTask
from app.observability.logging import logger

class SendEmailTask(BaseTask):
    """发送邮件任务"""
    
    async def execute(self, **kwargs: Dict[str, Any]) -> Any:
        """执行发送邮件任务"""
        email = kwargs.get("email")
        subject = kwargs.get("subject")
        content = kwargs.get("content")
        
        # 实际发送邮件逻辑
        logger.info(f"Sending email to {email} with subject: {subject}")
        # send_email(email, subject, content)
        
        return {"status": "success", "email": email}
```

**使用示例**：
```python
# 发布事件
from app.infrastructure.queue.connection import get_queue_producer

async def publish_user_created_event(user_id: int, email: str):
    """发布用户创建事件"""
    async with get_queue_producer() as producer:
        await producer.publish("user.created", {
            "user_id": user_id,
            "email": email
        })

# 消费事件
from app.infrastructure.queue.connection import get_queue_consumer
from app.tasks.email import SendEmailTask

async def consume_user_created_events():
    """消费用户创建事件"""
    email_task = SendEmailTask()
    
    async def handle_user_created(event_data):
        """处理用户创建事件"""
        user_id = event_data["user_id"]
        email = event_data["email"]
        
        # 发送欢迎邮件
        await email_task.execute(
            email=email,
            subject="Welcome to our platform",
            content=f"Hello, thank you for registering with us! Your user ID is {user_id}."
        )
    
    async with get_queue_consumer() as consumer:
        await consumer.subscribe("user.created", handle_user_created)
```

### 10. 插件架构设计

**核心作用**：支持架构扩展，允许动态加载插件

**设计特点**：
- 插件接口抽象
- 插件自动发现
- 插件生命周期管理
- 插件依赖管理

**模块架构图**：
```mermaid
graph TD
    subgraph 插件架构
        A[插件基类] --> B[认证插件]
        A --> C[日志插件]
        A --> D[监控插件]
        A --> E[自定义插件]
        
        F[插件管理器] --> G[插件发现]
        F --> H[插件注册]
        F --> I[插件初始化]
        F --> J[插件注销]
        
        G --> K[入口点扫描]
        G --> L[动态加载]
        
        H --> M[路由注册]
        H --> N[中间件注册]
        H --> O[事件监听]
    end
    
    FastAPI[FastAPI应用] --> F
    F --> FastAPI
    
    style A fill:#FF6B6B,stroke:#2D3436,stroke-width:3px,color:white,rx:8,ry:8
    style B fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style C fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style D fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style E fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style F fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style G fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style H fill:#E9ECEF,stroke:#2D3436,stroke-width:3px,color:#2D3436,rx:8,ry:8
    style I fill:#FF6B6B,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style J fill:#4ECDC4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style K fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style L fill:#96CEB4,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style M fill:#FF9FF3,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style N fill:#54A0FF,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
    style O fill:#FECA57,stroke:#2D3436,stroke-width:2px,color:#2D3436,rx:8,ry:8
    style FastAPI fill:#45B7D1,stroke:#2D3436,stroke-width:2px,color:white,rx:8,ry:8
```

**数据流转图**：
```mermaid
sequenceDiagram
    participant App as FastAPI应用
    participant PM as 插件管理器
    participant Discovery as 插件发现
    participant Loader as 插件加载
    participant Registry as 插件注册
    participant Plugin as 插件实例
    
    App->>PM: 初始化插件管理器
    PM->>Discovery: 发现插件
    Discovery->>Loader: 扫描入口点
    Loader->>Plugin: 加载插件类
    Plugin->>Loader: 返回插件实例
    Loader->>PM: 注册插件实例
    PM->>Registry: 注册插件
    Registry->>App: 向应用注册插件
    App->>PM: 应用运行
    App->>PM: 应用关闭
    PM->>Plugin: 注销插件
    Plugin->>PM: 插件清理
```

**关键实现**：
```python
# app/plugins/base.py
from abc import ABC, abstractmethod
from fastapi import FastAPI

class BasePlugin(ABC):
    """插件基类"""
    
    name: str
    version: str
    description: str
    
    @abstractmethod
    def register(self, app: FastAPI) -> None:
        """注册插件"""
        pass
    
    @abstractmethod
    def unregister(self) -> None:
        """注销插件"""
        pass

# app/plugins/manager.py
from fastapi import FastAPI
from app.plugins.base import BasePlugin
from typing import List
import pkg_resources

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: List[BasePlugin] = []
    
    def discover_plugins(self) -> None:
        """发现插件"""
        for entry_point in pkg_resources.iter_entry_points("fastapi.plugins"):
            try:
                plugin_class = entry_point.load()
                if issubclass(plugin_class, BasePlugin):
                    plugin = plugin_class()
                    self.plugins.append(plugin)
            except Exception as e:
                # 记录插件加载失败
                from app.observability.logging import logger
                logger.error(f"Failed to load plugin {entry_point.name}: {e}")
    
    def register_plugins(self, app: FastAPI) -> None:
        """注册所有插件"""
        for plugin in self.plugins:
            try:
                plugin.register(app)
            except Exception as e:
                # 记录插件注册失败
                from app.observability.logging import logger
                logger.error(f"Failed to register plugin {plugin.name}: {e}")
```

## 六、目录结构设计

```
fastapi_enterprise/
├── app/                     # 应用核心目录
│   ├── __init__.py
│   ├── main.py              # 应用入口（创建实例、注册所有组件）
│   ├── api/                 # API路由模块（按版本划分）
│   │   ├── __init__.py
│   │   ├── v1/              # v1版本API
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── users.py
│   │   └── v2/              # v2版本API
│   │       ├── __init__.py
│   │       └── users.py
│   ├── config/              # 配置模块
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── version.py
│   ├── dependencies/        # 依赖注入模块（通用依赖）
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── db.py
│   ├── domains/             # DDD领域模块
│   │   ├── __init__.py
│   │   ├── user/            # 用户领域
│   │   │   ├── __init__.py
│   │   │   ├── models.py          # 用户数据模型（实体）
│   │   │   ├── schemas.py         # 用户数据校验Schema
│   │   │   ├── services/          # 用户领域服务
│   │   │   │   ├── __init__.py
│   │   │   │   └── user_service.py    # 用户服务实现
│   │   │   └── repositories/      # 用户仓储层
│   │   │       ├── __init__.py
│   │   │       └── user_repository.py  # 用户仓储实现
│   │   ├── order/           # 订单领域
│   │   │   ├── __init__.py
│   │   │   ├── models.py          # 订单数据模型
│   │   │   ├── schemas.py         # 订单数据校验Schema
│   │   │   ├── services/          # 订单领域服务
│   │   │   │   ├── __init__.py
│   │   │   │   └── order_service.py   # 订单服务实现
│   │   │   └── repositories/      # 订单仓储层
│   │   │       ├── __init__.py
│   │   │       └── order_repository.py # 订单仓储实现
│   │   └── product/         # 商品领域
│   │       ├── __init__.py
│   │       ├── models.py          # 商品数据模型
│   │       ├── schemas.py         # 商品数据校验Schema
│   │       ├── services/          # 商品领域服务
│   │       │   ├── __init__.py
│   │       │   └── product_service.py  # 商品服务实现
│   │       └── repositories/      # 商品仓储层
│   │           ├── __init__.py
│   │           └── product_repository.py # 商品仓储实现
│   ├── infrastructure/      # 基础设施层
│   │   ├── __init__.py
│   │   ├── database/        # 数据库连接管理
│   │   ├── cache/           # 缓存模块
│   │   ├── queue/           # 消息队列
│   │   ├── logging/         # 日志模块
│   │   └── security/        # 安全模块
│   ├── middleware/          # 中间件模块
│   │   ├── __init__.py
│   │   ├── cors.py
│   │   ├── logging.py
│   │   └── rate_limiter.py
│   ├── observability/       # 观测性模块
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   └── tracing.py
│   ├── plugins/             # 插件架构
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── manager.py
│   ├── tasks/               # 异步任务模块
│   │   ├── __init__.py
│   │   └── base.py
│   ├── utils/               # 工具模块
│   │   ├── __init__.py
│   │   ├── cryptography.py
│   │   └── validator.py
│   └── exceptions/          # 自定义异常
│       ├── __init__.py
│       └── base.py
├── alembic/                 # 数据库迁移模块（Alembic）
├── tests/                   # 测试模块（按业务域组织）
│   ├── __init__.py
│   ├── conftest.py          # 测试夹具
│   ├── integration/         # 集成测试
│   ├── unit/                # 单元测试
│   └── utils/               # 测试工具
├── docs/                    # 文档模块
│   ├── api/                 # API文档
│   ├── architecture/        # 架构设计文档
│   └── deployment/          # 部署文档
├── scripts/                 # 脚本模块
│   ├── deploy.sh            # 部署脚本
│   ├── init_db.py           # 数据库初始化脚本
│   └── start_consumer.py    # 启动消费者脚本
├── plugins/                 # 插件目录
│   └── example_plugin/      # 示例插件
├── .env                     # 环境变量模板
├── .env.dev                 # 开发环境变量
├── .env.test                # 测试环境变量
├── .env.prod                # 生产环境变量
├── alembic.ini              # Alembic配置文件
├── pyproject.toml           # 项目配置
├── requirements.txt         # 核心依赖
├── requirements-dev.txt     # 开发依赖
└── README.md                # 项目文档
```

## 七、API版本控制设计

### 1. 版本控制策略

本架构支持多种API版本控制策略，推荐使用**URL路径版本控制**作为主要策略，同时支持**Header版本控制**作为兼容策略。

**URL路径版本控制**：
```
/api/v1/users
/api/v2/users
```

**Header版本控制**：
```
GET /api/users
X-API-Version: v1
```

### 2. 版本管理实现

```python
# app/config/version.py
from enum import Enum

class APIVersion(str, Enum):
    """API版本枚举"""
    V1 = "v1"
    V2 = "v2"

# 默认版本
DEFAULT_API_VERSION = APIVersion.V1
# 支持的版本列表
SUPPORTED_VERSIONS = [v.value for v in APIVersion]
```

```python
# app/api/__init__.py
from fastapi import APIRouter, FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.config.version import SUPPORTED_VERSIONS, DEFAULT_API_VERSION

def get_api_version(request: Request) -> str:
    """获取API版本"""
    # 从URL路径获取版本
    for version in SUPPORTED_VERSIONS:
        if request.url.path.startswith(f"/api/{version}"):
            return version
    # 从Header获取版本
    version_header = request.headers.get("X-API-Version")
    if version_header in SUPPORTED_VERSIONS:
        return version_header
    # 返回默认版本
    return DEFAULT_API_VERSION

# 主API路由器
api_router = APIRouter(prefix="/api")

# 注册版本路由
from app.api.v1 import api_router as v1_router
from app.api.v2 import api_router as v2_router

api_router.include_router(v1_router, prefix="/v1", tags=["v1"])
api_router.include_router(v2_router, prefix="/v2", tags=["v2"])
```

## 八、最佳实践

### 1. 代码组织最佳实践

- **按业务域组织代码**：使用DDD思想，将相关代码组织在同一个业务域目录下
- **接口抽象优先**：通过接口定义模块间的契约，实现解耦
- **依赖注入**：充分利用FastAPI的依赖注入系统，提高代码可测试性
- **类型安全**：使用Pydantic进行数据验证，确保类型安全
- **异步优先**：对IO密集型操作使用异步IO，提高并发性能

### 2. API设计最佳实践

- **RESTful设计**：遵循RESTful API设计原则
- **API版本控制**：使用URL路径版本控制（/api/v1/）
- **标准化响应格式**：统一API响应格式，包含code、message、data字段
- **分页设计**：对列表接口实现分页，支持page和page_size参数
- **过滤和排序**：支持通过查询参数进行过滤和排序
- **文档自动生成**：利用FastAPI的自动文档生成功能

### 3. 数据库设计最佳实践

- **ORM优先**：使用SQLAlchemy ORM进行数据库操作
- **数据库迁移**：使用Alembic管理数据库表结构变更
- **事务管理**：使用数据库事务确保数据一致性
- **索引优化**：为频繁查询的字段添加索引
- **连接池管理**：合理配置数据库连接池大小

### 4. 安全最佳实践

- **认证授权**：实现细粒度的认证授权机制
- **输入验证**：对所有输入进行严格验证
- **输出过滤**：对输出数据进行过滤，防止敏感信息泄露
- **加密传输**：使用HTTPS进行数据传输
- **加密存储**：对敏感数据进行加密存储
- **防止常见攻击**：防止SQL注入、XSS、CSRF等常见安全漏洞
- **定期安全审计**：定期进行安全审计和漏洞扫描

### 5. 测试策略

**测试分层**：
- **单元测试**：测试单个函数、类或模块
- **集成测试**：测试模块间的交互
- **API测试**：测试API端点的正确性
- **端到端测试**：测试整个系统的流程

**测试框架**：
- 使用pytest进行单元测试和集成测试
- 使用pytest-asyncio进行异步测试
- 使用httpx进行API测试

**测试覆盖率**：
- 单元测试覆盖率≥80%
- 关键业务逻辑覆盖率100%
- API测试覆盖率≥90%

### 6. 部署和DevOps最佳实践

**部署策略**：
- 支持多环境部署（开发、测试、生产）
- 容器化部署（Docker + Kubernetes）
- 持续集成和持续部署（CI/CD）
- 蓝绿部署或金丝雀发布

**监控和告警**：
- 集成Prometheus和Grafana进行监控
- 实现日志集中管理（ELK或Loki）
- 设置关键指标告警
- 定期性能分析

**DevOps工具链**：
- 代码管理：Git + GitHub/GitLab
- CI/CD：GitHub Actions或GitLab CI
- 基础设施即代码：Terraform或Ansible
- 容器编排：Kubernetes
- 监控告警：Prometheus + Grafana + Alertmanager

## 九、技术栈选型

| 技术/框架 | 版本 | 用途 |
|-----------|------|------|
| fastapi | >=0.125.0 | Web框架 |
| uvicorn | >=0.30.0 | ASGI服务器 |
| pydantic-settings | >=2.0.0 | 配置管理 |
| sqlalchemy | >=2.0.45 | ORM框架 |
| asyncpg | >=0.29.0 | PostgreSQL异步驱动 |
| python-jose | >=3.5.0 | JWT处理 |
| bcrypt | >=5.0.0 | 密码加密 |
| redis | >=5.0.0 | 缓存系统 |
| aioredis | >=2.0.1 | Redis异步客户端 |
| aio-pika | >=9.4.0 | RabbitMQ异步客户端 |
| alembic | >=1.10.0 | 数据库迁移 |
| pytest | >=9.0.2 | 测试框架 |
| pytest-asyncio | >=0.23.2 | 异步测试支持 |
| httpx | >=0.27.0 | HTTP客户端 |
| python-dotenv | >=1.2.1 | 环境变量管理 |
| python-json-logger | >=2.0.7 | JSON日志格式化 |
| prometheus-client | >=0.20.0 | 指标收集 |
| opentelemetry-sdk | >=1.24.0 | 分布式追踪 |

## 十、架构评估与优化建议

### 1. 架构优势

- ✅ **分层设计清晰**：各层职责明确，耦合度低
- ✅ **DDD领域驱动设计**：业务逻辑与技术实现分离，便于维护和扩展
- ✅ **插件架构**：支持动态扩展，便于功能定制
- ✅ **全面的安全保障**：支持多种认证授权方式，防止常见安全漏洞
- ✅ **良好的观测性**：提供全面的监控、追踪和日志功能
- ✅ **异步支持**：充分利用FastAPI的异步特性，提高并发性能
- ✅ **类型安全**：使用Pydantic进行数据验证，确保类型安全
- ✅ **可测试性**：设计便于测试的架构，支持多种测试方式

### 2. 架构优化建议

#### 2.1 短期优化建议

- **实现自动化测试**：完善单元测试、集成测试和API测试
- **优化数据库查询**：添加索引，优化查询性能
- **实现缓存策略**：对频繁访问的数据进行缓存
- **完善日志系统**：实现结构化日志，便于分析和监控

#### 2.2 中期优化建议

- **引入事件驱动架构**：使用消息队列处理异步事件
- **实现分布式追踪**：集成OpenTelemetry实现分布式追踪
- **优化部署策略**：实现蓝绿部署或金丝雀发布
- **完善监控告警**：设置关键指标告警，及时发现问题

#### 2.3 长期优化建议

- **支持多租户**：实现多租户架构，支持多个客户共享同一套系统
- **实现微服务架构**：将大型单体应用拆分为多个微服务
- **支持Serverless部署**：支持Serverless部署模式，降低运维成本
- **实现AI辅助功能**：集成AI功能，提高系统智能化水平

## 十一、总结

本FastAPI企业级架构设计指南提供了一个完整的、可扩展的架构设计，适合作为多个项目的通用轮子项目。该架构具有以下特点：

1. **合理性**：遵循分层设计、DDD领域驱动设计和模块化设计原则，职责划分清晰，耦合度低
2. **可扩展性**：支持插件架构，便于动态扩展功能，无需修改核心代码
3. **安全性**：提供全面的安全保障，防止常见安全漏洞
4. **观测性**：提供全面的监控、追踪和日志功能，便于运维和问题排查
5. **异步支持**：充分利用FastAPI的异步特性，提高并发性能
6. **类型安全**：使用Pydantic进行数据验证，确保类型安全
7. **可测试性**：设计便于测试的架构，支持多种测试方式

通过使用本架构，开发团队可以快速构建高质量、可扩展的FastAPI应用，减少重复设计和实现工作，专注于业务逻辑开发。同时，本架构支持多环境部署、API版本控制和持续集成持续部署，适合构建各种规模的企业级应用。

## 十二、TODO列表

### 1. 核心架构实现
- [ ] 实现配置管理模块，支持多环境配置
- [ ] 实现依赖注入模块，封装通用依赖
- [ ] 实现路由模块，支持API版本控制
- [ ] 实现服务层，基于DDD设计
- [ ] 实现仓储层，支持多种数据库

### 2. 安全模块实现
- [ ] 实现JWT认证
- [ ] 实现API Key认证
- [ ] 实现细粒度权限控制
- [ ] 实现输入验证和输出过滤

### 3. 观测性模块实现
- [ ] 实现结构化日志
- [ ] 实现请求追踪
- [ ] 实现性能监控
- [ ] 实现健康检查

### 4. 异步和消息队列实现
- [ ] 实现异步任务处理
- [ ] 实现消息队列集成
- [ ] 实现领域事件发布订阅

### 5. 插件架构实现
- [ ] 实现插件接口
- [ ] 实现插件自动发现
- [ ] 实现插件生命周期管理

### 6. 测试和部署
- [ ] 实现单元测试和集成测试
- [ ] 实现API测试
- [ ] 实现CI/CD流水线
- [ ] 实现容器化部署

### 7. 文档完善
- [ ] 编写详细的模块文档
- [ ] 编写API文档
- [ ] 编写部署文档
- [ ] 编写最佳实践指南

## 十三、参考资料

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [DDD领域驱动设计](https://domainlanguage.com/)
- [SQLAlchemy官方文档](https://docs.sqlalchemy.org/)
- [Pydantic官方文档](https://docs.pydantic.dev/)
- [Kubernetes官方文档](https://kubernetes.io/docs/)
- [Prometheus官方文档](https://prometheus.io/docs/)
- [Grafana官方文档](https://grafana.com/docs/)