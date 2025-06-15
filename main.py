import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from pydantic import BaseModel
from typing import Any
from dotenv import load_dotenv
import os

# 配置日誌
TUYA_LOGGER.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("---------------------------------------------------------------------------------------")

# 載入環境變數
load_dotenv()

# Tuya 配置
TUYA_ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
TUYA_ACCESS_SECRET = os.getenv("TUYA_ACCESS_SECRET")
TUYA_API_ENDPOINT = os.getenv("TUYA_API_ENDPOINT")
# TUYA_FINGERBOT_ID = os.getenv("TUYA_FINGERBOT_ID")

logger.info("Initialize FastAPI")
# print("Initialize FastAPI")
# 初始化 FastAPI
app = FastAPI(title="Tuya Fingerbot API")

logger.info("Initialize and connect TuyaOpenAPI")
# print("Initialize and connect TuyaOpenAPI")
# 初始化 TuyaOpenAPI
openapi = TuyaOpenAPI(TUYA_API_ENDPOINT, TUYA_ACCESS_ID, TUYA_ACCESS_SECRET)

# 定義 Lifespan 處理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時執行的邏輯
    logger.info("Connecting to Tuya API...")
    openapi.connect()
    logger.info(f"device token_info uid: {openapi.token_info.uid}, access_token: {openapi.token_info.access_token}")
    yield  # 應用運行期間
    # 關閉時執行的邏輯（可選）
    logger.info("Shutting down Tuya API connection...")

# 初始化 FastAPI，傳遞 lifespan
app = FastAPI(lifespan=lifespan)

# 定義請求模型
class CommandRequest(BaseModel):
    code: str
    value: Any

# API 端點
@app.get("/devices/{device_id}/functions")
async def get_device_functions(device_id: str):
    logger.info("/n")
    logger.info("get_device_functions")
    logger.info(f"device_id: {device_id}")
    """獲取設備指令集"""
    try:
        response = openapi.get(f"/v1.0/iot-03/devices/{device_id}/functions")
        if not response.get("success"):
            raise HTTPException(status_code=400, detail=response.get("msg", "Failed to get functions"))
        return response
    except Exception as e:
        logger.error(f"Error getting functions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices/{device_id}/status")
async def get_device_status(device_id: str):
    logger.info("/n")
    logger.info("get_device_status")
    logger.info(f"device_id: {device_id}")
    """獲取設備狀態"""
    try:
        response = openapi.get(f"/v1.0/iot-03/devices/{device_id}/status")
        if not response.get("success"):
            raise HTTPException(status_code=400, detail=response.get("msg", "Failed to get status"))
        return response
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/devices/{device_id}/commands")
async def send_command(device_id: str, command: CommandRequest):
    logger.info("/n")
    logger.info("send_command")
    logger.info(f"device_id: {device_id}, code: {command.code}, value: {command.value}")
    """發送控制指令"""
    try:
        # print(f"device_id: {device_id}, command: {command}, code: {command.code}, value: {command.value}")
        commands = {"commands": [{"code": command.code, "value": command.value}]}
        response = openapi.post(f"/v1.0/iot-03/devices/{device_id}/commands", commands)
        if not response.get("success"):
            raise HTTPException(status_code=400, detail=response.get("msg", "Failed to send command"))
        return response
    except Exception as e:
        logger.error(f"Error sending command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# @app.on_event("startup")
# async def startup_event():
#     """應用啟動時執行"""
#     logger.info("Connecting to Tuya API...")
#     openapi.connect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)