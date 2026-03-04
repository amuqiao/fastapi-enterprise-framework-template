import time
import asyncio
import aiohttp
import json
import datetime
import copy  # 引入 copy 模块用于深拷贝

# ================= 配置区域 =================
# url = "http://139.159.135.16:8000/api/v1/audit" # 测试环境
url = "http://10.51.6.215:8000/api/v1/audit"  # 本地环境

headers = {
    "Content-Type": "application/json",
    "accept": "application/json"
}

# 基础 payload 模板
base_payload = {
    "timeout": 600,
    "images": [
        {
            "image_id": "IMG_DEFAULT",  # 这里的值会被动态替换
            "image_name": "购售电合同",
            "image_type": "购售电合同",
            "image_url": "https://obs.cn-south-1.myhuaweicloud.com/aurora-prod-obs/2602/1113/ce1fb795f9f04419a5463f4ad9c29250?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20260211T054842Z&X-Amz-SignedHeaders=host&X-Amz-Expires=604800&X-Amz-Credential=7JLQ3J0JOA5C7PTFJFWO%2F20260211%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=791f38ab0136fd6fb21fc2d8c4a39b8ebec9ed28774b9516a84bdd69b7bbbef1",
            "object_id": "OBJ_003"
        }
    ],
    "method_list": [
        "denoise",
        "grayscale"
    ],
    "batch_mode": True
}

CONCURRENT_REQUESTS = 5
# 并发请求数量
RESULT_FILE = "pressure_test_results.txt"  # 结果保存的文件名


# ===========================================

async def send_request(session, index):
    """
    发送单个请求的异步函数
    """
    # 【关键修改】：使用 deepcopy，确保 images 列表也是独立的，互不影响
    current_payload = copy.deepcopy(base_payload)

    # 动态修改 order_no
    current_payload["order_no"] = str(index)

    # 动态修改 image_id (例如: IMG_1, IMG_2...)
    # 如果你想纯数字，可以改为: current_payload["images"][0]["image_id"] = str(index)
    current_payload["images"][0]["image_id"] = f"IMG_{index}"

    start_req_time = time.time()
    log_content = ""

    try:
        timeout = aiohttp.ClientTimeout(total=600)
        async with session.post(url, json=current_payload, headers=headers, timeout=timeout) as response:
            text = await response.text()
            duration = time.time() - start_req_time

            print(f"[完成] 请求: {index} | ID: IMG_{index} | 耗时: {duration:.2f}s | 状态: {response.status}")

            log_content = (
                f"============== 请求序号: {index} ==============\n"
                f"Image ID: IMG_{index}\n"
                f"请求时间: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
                f"HTTP状态码: {response.status}\n"
                f"耗时: {duration:.4f} 秒\n"
                f"响应内容: {text}\n"
                f"\n"
            )
            return log_content

    except Exception as e:
        duration = time.time() - start_req_time
        print(f"[错误] 请求: {index} | ID: IMG_{index} | 耗时: {duration:.2f}s | 错误: {e}")

        log_content = (
            f"============== 请求序号: {index} ==============\n"
            f"Image ID: IMG_{index}\n"
            f"请求时间: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            f"请求结果: 异常失败\n"
            f"耗时: {duration:.4f} 秒\n"
            f"错误详情: {str(e)}\n"
            f"\n"
        )
        return log_content


async def main():
    print(f"开始压测，目标: {url}")
    print(f"并发数: {CONCURRENT_REQUESTS}")
    print("-" * 30)

    start_time = time.time()

    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(1, CONCURRENT_REQUESTS + 1):
            task = asyncio.create_task(send_request(session, i))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

    total_time = time.time() - start_time

    print("-" * 30)
    print(f"请求全部结束，正在写入文件: {RESULT_FILE} ...")

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(f"压测总耗时: {total_time:.2f} 秒\n")
        f.write(f"并发数量: {CONCURRENT_REQUESTS}\n")
        f.write(f"测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n\n")

        for res in results:
            f.write(res)

    print(f"写入完成。总耗时: {total_time:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())