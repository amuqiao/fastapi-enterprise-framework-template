#!/usr/bin/env python3
import requests
import json

def send_feishu_message(webhook_url: str, message: str) -> dict:
    """使用飞书自定义机器人发送消息
    
    Args:
        webhook_url: 飞书机器人webhook地址
        message: 要发送的消息内容
        
    Returns:
        dict: 响应结果
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "code": -1,
            "msg": f"请求失败: {str(e)}",
            "data": {}
        }

def main():
    """主函数，接收用户输入并发送消息"""
    # 飞书机器人webhook地址
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/c4a51d72-f64c-46cf-9194-1aa78a11c22b"
    
    print("飞书机器人消息发送工具")
    print("请输入要发送的消息内容（输入'quit'退出）:")
    
    while True:
        try:
            # 接收用户输入
            message = input("> ")
            
            if message.lower() == 'quit':
                print("退出程序")
                break
            
            if not message.strip():
                print("消息内容不能为空，请重新输入")
                continue
            
            # 发送消息
            result = send_feishu_message(webhook_url, message)
            
            # 处理响应
            if result.get("code") == 0:
                print(f"消息发送成功！")
            else:
                print(f"消息发送失败: {result.get('msg', '未知错误')}")
                
        except KeyboardInterrupt:
            print("\n退出程序")
            break
        except Exception as e:
            print(f"程序异常: {str(e)}")
            break

if __name__ == "__main__":
    main()
