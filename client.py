# client.py

import requests
import json
import uuid
import os
import sys # 导入sys模块以使用exit()

def call_thermal_count_api(image_path: str):
    """
    调用 [S1_T1] 热成像无人艇快速检测 API。
    """
    api_url = "http://127.0.0.1:8000/v1/command/analyze_image/thermal_count"
    print(f"▶️  准备发送请求到 (S1_T1): {api_url}")
    
    request_data = {
        "command_id": f"CMD-{uuid.uuid4()}",
        "task_type": "THERMAL_USV_COUNT",
        "params": {"image_path": image_path}
    }
    
    print("Request Body:")
    print(json.dumps(request_data, indent=2))
    
    try:
        response = requests.post(api_url, json=request_data, timeout=10)
        
        print("\n◀️  收到服务器响应:")
        print(f"HTTP Status Code: {response.status_code}")
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))

        if response_json.get("status") == "SUCCESS":
            count = response_json.get("result", {}).get("detected_count", "N/A")
            print(f"\n✅ [S1_T1] 操作成功! 检测到的无人艇数量为: {count}")
        else:
            error_msg = response_json.get("error", {}).get("message", "未知错误")
            print(f"\n❌ [S1_T1] 操作失败! 原因: {error_msg}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ [S1_T1] 请求异常: {e}")


def call_visible_identify_api(image_path: str):
    """
    调用 [S1_T2] 可见光无人艇精准识别 API。
    """
    api_url = "http://127.0.0.1:8000/v1/command/analyze_image/visible_identify"
    print(f"▶️  准备发送请求到 (S1_T2): {api_url}")

    request_data = {
        "command_id": f"CMD-{uuid.uuid4()}",
        "task_type": "VISIBLE_USV_IDENTIFY",
        "params": {"image_path": image_path}
    }

    print("Request Body:")
    print(json.dumps(request_data, indent=2))

    try:
        response = requests.post(api_url, json=request_data, timeout=10)

        print("\n◀️  收到服务器响应:")
        print(f"HTTP Status Code: {response.status_code}")
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))

        if response_json.get("status") == "SUCCESS":
            detections = response_json.get("result", {}).get("detections", [])
            print(f"\n✅ [S1_T2] 操作成功! 共检测到 {len(detections)} 个目标。")
            for det in detections:
                print(f"  - ID: {det['identity']}, Box: {det['box_xyxy']}, Confidence: {det['confidence']}")
        else:
            error_msg = response_json.get("error", {}).get("message", "未知错误")
            print(f"\n❌ [S1_T2] 操作失败! 原因: {error_msg}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ [S1_T2] 请求异常: {e}")


if __name__ == "__main__":
    # --- 在这里配置你要测试的图片路径 ---
    # ‼️ 重要: 请确保下面的路径指向一个真实存在的文件。
    test_image_path = "./model_architecture.png" 

    # --- 新增：路径检查逻辑 ---
    # 在执行任何操作前，首先检查测试文件是否存在。
    if not os.path.exists(test_image_path):
        print("="*70)
        print(f"❌ 测试终止：指定的图片路径不存在！")
        print(f"   路径: '{test_image_path}'")
        print("\n   请打开 client.py 文件, 修改 `test_image_path` 变量的值,")
        print("   使其指向一个您电脑上真实存在的图片文件。")
        print("="*70)
        sys.exit() # 直接退出脚本，不执行后续API调用
            
    # --- 测试 [S1_T1] 热成像计数功能 ---
    print("--- 开始测试 [S1_T1]: 热成像计数 ---")
    call_thermal_count_api(test_image_path)
    print("\n" + "="*70 + "\n")

    # --- 测试 [S1_T2] 可见光识别功能 ---
    print("--- 开始测试 [S1_T2]: 可见光识别 ---")
    call_visible_identify_api(test_image_path)