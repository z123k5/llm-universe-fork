import os
import sys
import random
from typing import List

from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import  FastAPI
from fastapi.responses import JSONResponse

# 餐馆服务员接口

app = FastAPI()  # 创建 api 对象


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
    ret.append({"dishId": "1", "name": "鱼香肉丝", "price": "20", "info": "鱼香肉丝是一道传统川菜，属于川菜系，是一道以猪肉丝为主要食材制作而成的川菜。",
               "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"})
    ret.append({"dishId": "2", "name": "宫保鸡丁", "price": "25", "info": "宫保鸡丁是一道传统川菜，属于川菜系，是一道以鸡肉丁为主要食材制作而成的川菜。",
               "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"})
    ret.append({"dishId": "3", "name": "地三鲜", "price": "18", "info": "地三鲜是一道传统东北菜，属于东北菜系，是一道以茄子、土豆、青椒为主要食材制作而成的东北菜。",
               "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"})
    ret.append({"dishId": "4", "name": "红烧肉", "price": "30", "info": "红烧肉是一道传统川菜，属于川菜系，是一道以猪肉为主要食材制作而成的川菜。",
               "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"})
    ret.append({"dishId": "5", "name": "酸辣土豆丝", "price": "15", "info": "酸辣土豆丝是一道传统川菜，属于川菜系，是一道以土豆丝为主要食材制作而成的川菜。",
               "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"})
    # 将ret转为字符串返回

    return JSONResponse(jsonable_encoder(ret))


@app.api_route("/api/v1/appendOrder", methods=["GET", "POST"])
async def append_order(order: List[dict]):
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

    return JSONResponse(jsonable_encoder({"status": "true", "msg": "success"}))


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
    return JSONResponse(jsonable_encoder({"num": "10", "msg": "success"}))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
