import lark_oapi as lark
from lark_oapi import Client, LogLevel, EventDispatcherHandler
from lark_oapi.api.im.v1 import *
import json
import threading
from app.infrastructure.events import event_bus
from app.infrastructure.events.event import EventType, Event


class FeishuMessageReceivedEvent(Event):
    """飞书消息接收事件"""
    
    def __init__(self, message_id: str, chat_id: str, chat_type: str, content: str, sender: dict):
        super().__init__(
            event_type=EventType.FEISHU_MESSAGE_RECEIVED,
            data={
                "message_id": message_id,
                "chat_id": chat_id,
                "chat_type": chat_type,
                "content": content,
                "sender": sender
            }
        )


class FeishuBotService:
    """飞书机器人服务类，用于处理飞书消息的接收和发送"""
    
    def __init__(self, app_id: str, app_secret: str, log_level: str = "DEBUG"):
        """初始化飞书机器人服务
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            log_level: 日志级别，默认为DEBUG
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.log_level = getattr(LogLevel, log_level.upper())
        self.client = None
        self.ws_client = None
        self.event_handler = None
        self.thread = None
        self._running = False
    
    def init(self):
        """初始化飞书机器人服务，创建客户端和事件处理器"""
        # 1. 创建事件处理器
        self.event_handler = EventDispatcherHandler.builder("", "")
        self.event_handler = self.event_handler.register_p2_im_message_receive_v1(self.handle_message)
        self.event_handler = self.event_handler.build()
        
        # 2. 创建API客户端（用于发送消息）
        self.client = Client.builder().app_id(self.app_id).app_secret(self.app_secret).build()
        
        # 3. 创建WebSocket客户端（用于接收消息）
        self.ws_client = lark.ws.Client(
            self.app_id,
            self.app_secret,
            event_handler=self.event_handler,
            log_level=self.log_level,
        )
    
    def _run(self):
        """在单独线程中运行的方法"""
        if self.ws_client:
            try:
                self.ws_client.start()
            except Exception as e:
                print(f"飞书机器人运行出错: {e}")
    
    def start(self):
        """启动飞书机器人服务，开始监听消息"""
        if not self._running and self.ws_client:
            self._running = True
            # 在单独的线程中启动飞书机器人服务
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
    
    def stop(self):
        """停止飞书机器人服务"""
        if self._running and self.ws_client:
            self._running = False
            try:
                self.ws_client.stop()
                # 等待线程结束
                if self.thread and self.thread.is_alive():
                    self.thread.join(timeout=5.0)
            except Exception as e:
                print(f"停止飞书机器人服务时出错: {e}")
            finally:
                self.thread = None
    
    def handle_message(self, data: P2ImMessageReceiveV1) -> None:
        """处理接收到的飞书消息
        
        Args:
            data: 飞书消息数据
        """
        # 解析消息内容
        res_content = ""
        if data.event.message.message_type == "text":
            try:
                res_content = json.loads(data.event.message.content)["text"]
            except (json.JSONDecodeError, KeyError):
                res_content = "解析消息失败"
        else:
            res_content = "解析消息失败，请发送文本消息"
        
        # 发布飞书消息事件
        event = FeishuMessageReceivedEvent(
            message_id=data.event.message.message_id,
            chat_id=data.event.message.chat_id,
            chat_type=data.event.message.chat_type,
            content=res_content,
            sender=data.event.sender.to_dict() if hasattr(data.event.sender, 'to_dict') else str(data.event.sender)
        )
        event_bus.publish(event)
        
        # 回复消息
        self.reply_message(data.event.message.message_id, res_content)
    
    def reply_message(self, message_id: str, content: str, msg_type: str = "text") -> None:
        """回复飞书消息
        
        Args:
            message_id: 要回复的消息ID
            content: 回复的内容
            msg_type: 消息类型，默认为text
        """
        # 构建回复内容
        reply_content = json.dumps({
            "text": f"收到你发送的消息：{content}\nReceived message: {content}"
        })
        
        # 构建回复请求
        request = ReplyMessageRequest.builder().message_id(message_id).request_body(ReplyMessageRequestBody.builder().content(reply_content).msg_type(msg_type).build()).build()
        
        # 发送回复
        response = self.client.im.v1.message.reply(request)
        if not response.success():
            raise Exception(f"Reply message failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
    
    def send_message(self, receive_id: str, receive_id_type: str, content: str, msg_type: str = "text") -> None:
        """发送飞书消息
        
        Args:
            receive_id: 接收者ID
            receive_id_type: 接收者ID类型，如open_id, user_id, chat_id
            content: 消息内容
            msg_type: 消息类型，默认为text
        """
        # 构建发送请求
        request = CreateMessageRequest.builder().receive_id_type(receive_id_type).request_body(CreateMessageRequestBody.builder().receive_id(receive_id).msg_type(msg_type).content(content).build()).build()
        
        # 发送消息
        response = self.client.im.v1.message.create(request)
        if not response.success():
            raise Exception(f"Send message failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
