from abc import ABC, abstractmethod
from typing import Any, Generator, Dict


class DatabaseConnection(ABC):
    """数据库连接基类"""

    @abstractmethod
    def connect(self) -> Any:
        """建立数据库连接"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开数据库连接"""
        pass

    @abstractmethod
    def get_session(self) -> Generator[Any, None, None]:
        """获取数据库会话"""
        pass


class DatabaseManager:
    """数据库管理器，管理多个数据库连接"""

    def __init__(self):
        self._connections: Dict[str, DatabaseConnection] = {}

    def register(self, name: str, connection: DatabaseConnection) -> None:
        """注册数据库连接"""
        self._connections[name] = connection

    def get(self, name: str) -> DatabaseConnection:
        """获取数据库连接"""
        if name not in self._connections:
            raise ValueError(f"Database connection '{name}' not registered")
        return self._connections[name]

    def connect_all(self) -> None:
        """连接所有数据库"""
        for name, connection in self._connections.items():
            connection.connect()

    def disconnect_all(self) -> None:
        """断开所有数据库连接"""
        for name, connection in self._connections.items():
            connection.disconnect()


# 全局数据库管理器实例
database_manager = DatabaseManager()
