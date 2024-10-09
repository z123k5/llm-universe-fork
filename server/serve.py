import datetime
import os
import sys
import random
from typing import List
import ast

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import  FastAPI, Request
from fastapi.responses import JSONResponse

# 根据时间生成随机数种子
random.seed(datetime.datetime.now())
# 餐馆服务员接口

app = FastAPI()  # 创建 api 对象

# CORS 设定只允许localhost访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dish = [
    {"dishId": "1", "name": "鱼香肉丝", "price": "20", "info": "鱼香肉丝是一道传统川菜，属于川菜系，是一道以猪肉丝为主要食材制作而成的川菜。"},
    {"dishId": "2", "name": "宫保鸡丁", "price": "25", "info": "宫保鸡丁是一道传统川菜，属于川菜系，是一道以鸡肉丁为主要食材制作而成的川菜。"},
    {"dishId": "3", "name": "地三鲜", "price": "18", "info": "地三鲜是一道传统东北菜，属于东北菜系，是一道以茄子、土豆、青椒为主要食材制作而成的东北菜。"},
    {"dishId": "4", "name": "红烧肉", "price": "30", "info": "红烧肉是一道传统川菜，属于川菜系，是一道以猪肉为主要食材制作而成的川菜。"},
    {"dishId": "5", "name": "酸辣土豆丝", "price": "15", "info": "酸辣土豆丝是一道传统川菜，属于川菜系，是一道以土豆丝为主要食材制作而成的川菜。"},
]

# {userId, orderId, sitNum, status, [dishId1, dishId2, ...]}}
order = []

@app.api_route("/api/v1/menu", methods=["GET", "POST"])
async def read_menu_price():
    """Route to get menu price

    Args:
        dishId (int): _description_

    Returns:
        _type_: _description_
    """
    ret = []

    """返回数据格式
    dishId | string (菜品编号) 
name | string (菜品名称)
price | string (价格)
info | string (描述)
avatar | string (图像路径)
"""
    return JSONResponse(jsonable_encoder(dish))


@app.api_route("/api/v1/querySit", methods=["GET", "POST"])
async def query_sit():
    """Route to query sit

    Returns:
        _type_: _description_
查询参数表:
None
返回值 (JSON object):
num | string (空闲座位数量)
msg | string (结果描述)
    """
    return JSONResponse(jsonable_encoder({"num": random.randint(1, 10), "msg": "获取座位数量成功"}))

@app.api_route("/api/v1/appendOrder", methods=["GET", "POST"])
async def append_order(request: Request):
    """Route to append order

    Args:
        order (List[dict]): _description_

    Returns:
        _type_: _description_
    
    查询参数表:
dishId | array[string] (菜品编号数组) | 必须
name | array[string] (菜品名称数组) | 必须
返回值 (JSON object):
status | "true" 如果成功 "false" 如果失败
msg | string (订单结果描述)
    """
    userId = request.query_params.get("userId")
    dishId = request.query_params.get("dishId")
    sitNum = request.query_params.get("sitNum")

    if not sitNum:
        sitNum = 0

    if not userId or not dishId:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，需要用户Id、菜品Id参数"}))
    
    userId = ast.literal_eval(userId)
    dishId = ast.literal_eval(dishId)

    if not isinstance(dishId, list) or not isinstance(userId, int):
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，参数类型错误"}))
    
    if not isinstance(dishId, list):
        dishId = [dishId,]
        
    if len(dishId) == 0:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，未提供菜品"}))
    
    for i in range(len(dishId)):
        # 从dish中查找dishId
        if int(dishId[i]) < 1 or not dish[int(dishId[i])-1]:
            return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，找不到菜品:dishId:{}".format(dishId[i])}))
        
    order.append({"userId": userId, "orderId": random.randint(1000, 3000), "orderNum": len(dishId), "sitNum": sitNum, "status": "true", "dishes": [dishId[i] for i in range(len(dishId))]})

    # 订单超过10个，删除第一个
    if len(order) > 10:
        order.pop(0)


    return JSONResponse(jsonable_encoder({"status": "true", "msg": "提交订单成功", "orderId": order[-1]["orderId"]}))


@app.api_route("/api/v1/payOrder", methods=["GET", "POST"])
async def pay_order(request: Request):
    """Route to pay order

    Returns:
        _type_: _description_
    """
    userId = request.query_params.get("userId")
    orderId = request.query_params.get("orderId")

    if not userId or not orderId:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "支付失败，需要用户Id、订单Id参数"}))
    
    userId = ast.literal_eval(userId)
    orderId = ast.literal_eval(orderId)

    if not isinstance(orderId, int) or not isinstance(userId, int):
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，参数类型错误"}))
        
    deleted = False
    for i in range(len(order)):
        if order[i]["orderId"] == orderId:
            order.pop(i)
            deleted = True
    if deleted:
        return JSONResponse(jsonable_encoder({"status": "true", "msg": "微信付款码生成成功，请扫码支付"}))

    return JSONResponse(jsonable_encoder({"status": "false", "msg": "支付失败，用户或订单不存在"}))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
