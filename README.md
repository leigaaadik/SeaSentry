# SeaSentry: Cooperative Maritime Vision API

> A FastAPI-based RESTful service demo for cooperative maritime target recognition, simulating vision tasks for UAVs and USVs.

## About The Project

**SeaSentry** is a demonstration project of a RESTful API service built with Python, FastAPI, and PyTorch. It is designed to simulate a real-world visual recognition service for maritime scenarios. Based on a predefined API specification, it receives commands to analyze specified images and returns results in a standardized JSON format.

The project consists of two main components:

1.  **`server.py`**: A web server built with **FastAPI**. It exposes API endpoints to handle image analysis tasks. For each task, it invokes a mock backend algorithm (using either a PyTorch MLP or a random generator) to process the request and returns a structured JSON response.
2.  **`client.py`**: A command-line client script that demonstrates how to interact with the server's API. It constructs compliant request payloads, sends HTTP requests, and then parses and prints the results received from the server.

## Implemented Features

This demo currently implements two core functions from the "UAV/USV Cooperative USV Recognition" scenario:

*   **[S1_T1] Thermal-based USV Quick Detection**: Analyzes a thermal image to return the total count of detected Unmanned Surface Vehicles (USVs).
*   **[S2_T2] Visible-light-based USV Precise Identification**: Analyzes a visible-light image to return the identity, bounding box, and confidence score for each identified USV.

## Project Structure

```.
├── server.py   # FastAPI server application
├── client.py   # Client script for testing the API
└── README.md   # This documentation
```

## Getting Started

### Prerequisites

*   Python 3.7+
*   Pip package manager

### Installation

1.  Clone the repository or download the source code.
2.  Install the required Python libraries by running the following command in your terminal:
    ```bash
    pip install "fastapi[all]" torch torchvision Pillow requests
    ```
    > `fastapi[all]` installs FastAPI, Uvicorn (the ASGI server), and other recommended dependencies.

## How to Run and Test

Please use two separate terminal windows to run the server and the client.

### Step 1: Configure the Client

Before running the test, you **must** configure the client to point to a valid image file on your local machine.

1.  Open `client.py` in your code editor.
2.  Locate the following line:
    ```python
    # ‼️ IMPORTANT: Make sure this path points to a real file on your system.
    test_image_path = "./model_architecture.png" 
    ```
3.  Replace the path string `"./model_architecture.png"` with the **absolute path to an image file** on your computer.

### Step 2: Start the API Server

1.  Open your **first terminal** window.
2.  Navigate to the project's root directory.
3.  Run the following command to start the server:
    ```bash
    uvicorn server:app --reload
    ```
    *   `server`: Refers to the `server.py` file.
    *   `app`: Refers to the `app = FastAPI()` instance created in `server.py`.
    *   `--reload`: Enables auto-reloading, which restarts the server whenever you save changes to the code.

4.  You should see output indicating that the server is running, like `Uvicorn running on http://127.0.0.1:8000`. **Keep this terminal window open.**

### Step 3: Run the Client to Test the API

1.  Open a **second terminal** window.
2.  Navigate to the project's root directory.
3.  Execute the client script:
    ```bash
    python client.py
    ```

4.  The client terminal will display detailed output, including the request payloads being sent, the responses received from the server, and the final results for both API calls. Simultaneously, the server terminal will show corresponding logs for each incoming request.

## API Endpoints

### Interactive API Documentation (Swagger UI)

This project leverages FastAPI's built-in support for automatic interactive API documentation. Once the server is running, you can access it by navigating to the following URL in your web browser:

> **http://127.0.0.1:8000/docs**

This interface allows you to explore all API endpoints, view their schemas, and even send test requests directly from your browser.

---

### 1. Thermal-based USV Quick Detection

*   **Description**: Analyzes a thermal image to return the total count of detected USVs.
*   **Method**: `POST`
*   **Endpoint**: `/v1/command/analyze_image/thermal_count`
*   **Request Body**:
    ```json
    {
      "command_id": "CMD-...",
      "task_type": "THERMAL_USV_COUNT",
      "params": {
        "image_path": "/path/to/your/image.tiff"
      }
    }
    ```
*   **Success Response**:
    ```json
    {
      "request_command_id": "CMD-...",
      "status": "SUCCESS",
      "timestamp_utc": "...",
      "result": {
        "detected_count": 2
      }
    }
    ```

---

### 2. Visible-light-based USV Precise Identification

*   **Description**: Analyzes a visible-light image to return detailed information for each identified USV.
*   **Method**: `POST`
*   **Endpoint**: `/v1/command/analyze_image/visible_identify`
*   **Request Body**:
    ```json
    {
      "command_id": "CMD-...",
      "task_type": "VISIBLE_USV_IDENTIFY",
      "params": {
        "image_path": "/path/to/your/image.jpg"
      }
    }
    ```
*   **Success Response**:
    ```json
    {
      "request_command_id": "CMD-...",
      "status": "SUCCESS",
      "timestamp_utc": "...",
      "result": {
        "detections": [
          {
            "identity": "USV_1",
            "box_xyxy":,
            "confidence": 0.98
          }
        ]
      }
    }
    ```


---

# SeaSentry：协同式海事视觉API

> 一个基于FastAPI的、用于协同海事目标识别的RESTful服务演示，模拟了无人机(UAV)和无人艇(USV)的视觉任务。

## 关于项目

**SeaSentry** 是一个使用 Python、FastAPI 和 PyTorch 构建的RESTful API服务演示项目。它旨在模拟一个真实世界的海事场景视觉识别服务。该服务根据一份预定义的API规范，接收指令以分析指定的图像，并以标准化的JSON格式返回结果。

该项目包含两个核心部分：

1.  **`server.py`**: 一个使用 **FastAPI** 构建的Web服务器。它开放了多个API端点，用于处理图像分析任务。对于每个任务，它会调用一个模拟的后端算法（使用PyTorch MLP或随机数生成器）来处理请求，并返回结构化的JSON响应。
2.  **`client.py`**: 一个命令行客户端脚本，用于演示如何与服务器的API进行交互。它会构造符合规范的请求体，发送HTTP请求，然后解析并打印从服务器收到的结果。

## 已实现功能

本演示项目当前实现了“无人机/艇协同对艇识别”场景中的两个核心功能：

*   **[S1_T1] 基于热成像的无人艇快速检测**: 分析一张热成像图片，返回图中检测到的无人水面载具（USV）的总数。
*   **[S2_T2] 基于可见光的无人艇精准识别**: 分析一张可见光图片，返回图中每艘被识别的无人艇的ID、边界框和置信度分数。

## 项目结构

```
.
├── server.py   # FastAPI 服务器应用
├── client.py   # 用于测试API的客户端脚本
└── README.md   # 本文档
```

## 开始使用

### 环境要求

*   Python 3.7+
*   Pip 包管理器

### 安装依赖

1.  克隆本仓库或下载源代码。
2.  在您的终端中运行以下命令，以安装所有必需的Python库：
    ```bash
    pip install "fastapi[all]" torch torchvision Pillow requests
    ```
    > `fastapi[all]` 会安装 FastAPI、Uvicorn (ASGI服务器) 以及其他推荐的依赖项。

## 如何运行与测试

请使用两个独立的终端窗口来分别运行服务器和客户端。

### 第一步：配置客户端

在开始测试之前，您**必须**配置客户端，使其指向您本地机器上的一个有效图片文件。

1.  在您的代码编辑器中打开 `client.py` 文件。
2.  找到下面这行代码：
    ```python
    # ‼️ 重要：请确保此路径指向您系统上的一个真实文件。
    test_image_path = "./model_architecture.png" 
    ```
3.  将路径字符串 `"./model_architecture.png"` **替换为您电脑上任意一张图片的绝对路径**。

### 第二步：启动API服务器

1.  打开您的 **第一个终端** 窗口。
2.  切换到本项目的根目录。
3.  运行以下命令来启动服务器：
    ```bash
    uvicorn server:app --reload
    ```
    *   `server`: 指的是 `server.py` 文件。
    *   `app`: 指的是在 `server.py` 中创建的 `app = FastAPI()` 实例。
    *   `--reload`: 启用自动重载功能，当您修改并保存代码后，服务器会自动重启。

4.  您应该能看到类似 `Uvicorn running on http://127.0.0.1:8000` 的输出，表明服务器正在运行。**请保持此终端窗口开启。**

### 第三步：运行客户端以测试API

1.  打开一个 **新的（第二个）终端** 窗口。
2.  切换到本项目的根目录。
3.  执行客户端脚本：
    ```bash
    python client.py
    ```

4.  客户端终端将会显示详细的输出，包括正在发送的请求体、从服务器收到的响应，以及两个API调用的最终结果。同时，服务器终端也会显示相应的请求日志。

## API 接口介绍

### 交互式API文档 (Swagger UI)

本项目利用了FastAPI内置的自动交互式API文档功能。在服务器运行后，您可以通过在浏览器中访问以下URL来查看：

> **http://127.0.0.1:8000/docs**

这个界面允许您浏览所有API端点，查看它们的结构，甚至直接在浏览器中发送测试请求。

---

### 1. 基于热成像的无人艇快速检测

*   **功能描述**: 分析一张热成像图片，返回检测到的无人艇总数。
*   **请求方法**: `POST`
*   **接口地址**: `/v1/command/analyze_image/thermal_count`
*   **请求体**:
    ```json
    {
      "command_id": "CMD-...",
      "task_type": "THERMAL_USV_COUNT",
      "params": {
        "image_path": "/path/to/your/image.tiff"
      }
    }
    ```
*   **成功响应**:
    ```json
    {
      "request_command_id": "CMD-...",
      "status": "SUCCESS",
      "timestamp_utc": "...",
      "result": {
        "detected_count": 2
      }
    }
    ```

---

### 2. 基于可见光的无人艇精准识别

*   **功能描述**: 分析一张可见光图片，返回每艘被识别的无人艇的详细信息。
*   **请求方法**: `POST`
*   **接口地址**: `/v1/command/analyze_image/visible_identify`
*   **请求体**:
    ```json
    {
      "command_id": "CMD-...",
      "task_type": "VISIBLE_USV_IDENTIFY",
      "params": {
        "image_path": "/path/to/your/image.jpg"
      }
    }
    ```
*   **成功响应**:
    ```json
    {
      "request_command_id": "CMD-...",
      "status": "SUCCESS",
      "timestamp_utc": "...",
      "result": {
        "detections": [
          {
            "identity": "USV_1",
            "box_xyxy":,
            "confidence": 0.98
          }
        ]
      }
    }
    ```

