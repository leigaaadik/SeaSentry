# server.py

# how to run the code?
# uvicorn server:app --reload

# --- 核心依赖 ---
import os
import datetime
import random
from typing import Union, List

# --- FastAPI 和 Pydantic 依赖 ---
from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field

# --- 机器学习和图像处理依赖 ---
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# ==============================================================================
# 1. 定义数据模型 (与API文档中的JSON结构完全对应)
# ==============================================================================

# --- 通用模型 ---
class CommandParams(BaseModel):
    """对应指令报文中的 "params" 部分"""
    image_path: str

class AnalyzeImageRequest(BaseModel):
    """对应完整的指令报文 (Request Body)"""
    command_id: str
    task_type: str
    params: CommandParams

class ErrorPayload(BaseModel):
    """对应失败响应报文中的 "error" 部分"""
    code: int
    message: str

class FailureResponse(BaseModel):
    """对应完整的失败响应报文"""
    request_command_id: str
    status: str = "FAILURE"
    timestamp_utc: str
    error: ErrorPayload

# --- [S1_T1] thermal_count 的特定模型 ---
class S1_T1_SuccessResult(BaseModel):
    detected_count: int

class S1_T1_SuccessResponse(BaseModel):
    request_command_id: str
    status: str = "SUCCESS"
    timestamp_utc: str
    result: S1_T1_SuccessResult

### 新增 [S1_T2] visible_identify 的特定模型 ###
class Detection(BaseModel):
    """单个检测结果的模型"""
    identity: str
    box_xyxy: List[int] = Field(..., min_items=4, max_items=4)
    confidence: float

class S1_T2_SuccessResult(BaseModel):
    detections: List[Detection]

class S1_T2_SuccessResponse(BaseModel):
    request_command_id: str
    status: str = "SUCCESS"
    timestamp_utc: str
    result: S1_T2_SuccessResult
# --- 模型定义结束 ---


# ==============================================================================
# 2. 定义核心的算法与模型
# ==============================================================================

# --- [S1_T1] 的核心算法 (保持不变) ---
class SimpleMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleMLP, self).__init__()
        self.layers = nn.Sequential(nn.Linear(input_size, hidden_size), nn.ReLU(), nn.Linear(hidden_size, output_size))
    def forward(self, x):
        return self.layers(x)

def thermal_usv_detection_with_mlp(image_path: str) -> int:
    print(f"--- [算法核心 S1_T1] 正在分析图片: {image_path} ---")
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found or access denied.")
    try:
        preprocess = transforms.Compose([transforms.Grayscale(num_output_channels=1), transforms.Resize((28, 28)), transforms.ToTensor()])
        img = Image.open(image_path)
        input_vector = preprocess(img).view(1, -1)
        model = SimpleMLP(input_size=28*28, hidden_size=64, output_size=1)
        model.eval()
        with torch.no_grad():
            raw_output = model(input_vector)
        detected_count = round(abs(raw_output.item()))
        print(f"--- [算法核心 S1_T1] 分析完成，检测数量为: {detected_count} ---")
        return detected_count
    except (IOError, Image.UnidentifiedImageError) as e:
        print(f"--- [算法核心 S1_T1] 错误: 处理图片时发生错误: {e}")
        raise IOError(f"Failed to process image file: {e}")

### 新增 [S1_T2] 的核心算法函数 ###
def visible_usv_identification(image_path: str) -> List[Detection]:
    """
    模拟的可见光无人艇精准识别函数。
    - 检查文件是否存在。
    - 如果存在，返回一个包含随机数量(0到2个)的、符合格式的检测结果列表。
    """
    print(f"--- [算法核心 S1_T2] 正在分析图片: {image_path} ---")
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found or access denied.")
    
    # 模拟随机检测到 0 到 2 艘无人艇
    num_detections = random.randint(0, 2)
    results = []
    
    if num_detections == 0:
        print("--- [算法核心 S1_T2] 分析完成，未检测到任何目标。 ---")
        return results

    for i in range(num_detections):
        # 生成随机但合理的坐标和置信度
        x1 = random.randint(100, 500)
        y1 = random.randint(100, 500)
        x2 = x1 + random.randint(100, 200)
        y2 = y1 + random.randint(100, 150)
        confidence = round(random.uniform(0.85, 0.99), 2)
        
        detection_result = Detection(
            identity=f"USV_{i+1}",
            box_xyxy=[x1, y1, x2, y2],
            confidence=confidence
        )
        results.append(detection_result)
        
    print(f"--- [算法核心 S1_T2] 分析完成，检测到 {len(results)} 个目标。 ---")
    return results
# --- 算法定义结束 ---


# ==============================================================================
# 3. 创建 FastAPI 应用实例
# ==============================================================================
app = FastAPI(
    title="视觉识别算法服务",
    description="实现了S1_T1和S1_T2功能的RESTful API。",
    version="1.2.0"
)

# ==============================================================================
# 4. 创建 API 端点 (Endpoint)
# ==============================================================================

# --- [S1_T1] 的 API 端点 (保持不变) ---
@app.post("/v1/command/analyze_image/thermal_count",
          response_model=Union[S1_T1_SuccessResponse, FailureResponse],
          tags=["场景1：协同对艇识别"])
async def analyze_thermal_image_for_usv_count(request: AnalyzeImageRequest, response: Response):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    try:
        count = thermal_usv_detection_with_mlp(request.params.image_path)
        success_payload = S1_T1_SuccessResponse(
            request_command_id=request.command_id,
            timestamp_utc=timestamp,
            result=S1_T1_SuccessResult(detected_count=count)
        )
        return success_payload
    except (FileNotFoundError, IOError) as e:
        error_code = 4041 if isinstance(e, FileNotFoundError) else 4221
        response.status_code = status.HTTP_404_NOT_FOUND if isinstance(e, FileNotFoundError) else status.HTTP_422_UNPROCESSABLE_ENTITY
        failure_payload = FailureResponse(
            request_command_id=request.command_id,
            timestamp_utc=timestamp,
            error=ErrorPayload(code=error_code, message=str(e))
        )
        return failure_payload
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FailureResponse(request_command_id=request.command_id, timestamp_utc=timestamp, error=ErrorPayload(code=5000, message=str(e)))


### 新增 [S1_T2] 的 API 端点 ###
@app.post("/v1/command/analyze_image/visible_identify",
          response_model=Union[S1_T2_SuccessResponse, FailureResponse],
          tags=["场景1：协同对艇识别"])
async def analyze_visible_image_for_usv_identification(request: AnalyzeImageRequest, response: Response):
    """
    功能ID: S1_T2
    分析一张指定路径下的可见光图片，识别并定位其中的特定无人艇。
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    # 简单的任务类型校验
    if request.task_type != "VISIBLE_USV_IDENTIFY":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return FailureResponse(
            request_command_id=request.command_id,
            timestamp_utc=timestamp,
            error=ErrorPayload(code=4001, message=f"Invalid task_type '{request.task_type}', expected 'VISIBLE_USV_IDENTIFY'.")
        )
        
    try:
        # 调用新的核心处理函数
        detections_list = visible_usv_identification(request.params.image_path)
        
        # 构建成功的响应报文
        success_payload = S1_T2_SuccessResponse(
            request_command_id=request.command_id,
            timestamp_utc=timestamp,
            result=S1_T2_SuccessResult(detections=detections_list)
        )
        return success_payload

    except (FileNotFoundError, IOError) as e:
        error_code = 4041 if isinstance(e, FileNotFoundError) else 4221
        response.status_code = status.HTTP_404_NOT_FOUND if isinstance(e, FileNotFoundError) else status.HTTP_422_UNPROCESSABLE_ENTITY
        failure_payload = FailureResponse(
            request_command_id=request.command_id,
            timestamp_utc=timestamp,
            error=ErrorPayload(code=error_code, message=str(e))
        )
        return failure_payload
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FailureResponse(request_command_id=request.command_id, timestamp_utc=timestamp, error=ErrorPayload(code=5000, message=str(e)))