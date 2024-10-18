import datetime
import os
import sys
import numpy as np
import random
from typing import List
import ast

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
# 分词
import jieba


# 根据时间生成随机数种子
random.seed(datetime.datetime.now())

# 机场订票服务助理接口

# 初始化分词器
jieba.initialize()


app = FastAPI()  # 创建 api 对象

# CORS 设定只允许localhost访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stations = [
    {"stationName": "北京首都国际机场", "stationCode": "PEK"},
    {"stationName": "上海浦东国际机场", "stationCode": "PVG"},
    {"stationName": "广州白云国际机场", "stationCode": "CAN"},
    {"stationName": "深圳宝安国际机场", "stationCode": "SZX"},
    {"stationName": "成都双流国际机场", "stationCode": "CTU"},
    {"stationName": "重庆江北国际机场", "stationCode": "CKG"},
    {"stationName": "杭州萧山国际机场", "stationCode": "HGH"},
    {"stationName": "武汉天河国际机场", "stationCode": "WUH"},
    {"stationName": "西安咸阳国际机场", "stationCode": "XIY"},
    {"stationName": "青岛流亭国际机场", "stationCode": "TAO"},
    {"stationName": "南京禄口国际机场", "stationCode": "NKG"},
    {"stationName": "厦门高崎国际机场", "stationCode": "XMN"},
    {"stationName": "大连周水子国际机场", "stationCode": "DLC"},
    {"stationName": "长沙黄花国际机场", "stationCode": "CSX"},
    {"stationName": "郑州新郑国际机场", "stationCode": "CGO"},
    {"stationName": "福州长乐国际机场", "stationCode": "FOC"},
    {"stationName": "沈阳桃仙国际机场", "stationCode": "SHE"},
    {"stationName": "昆明长水国际机场", "stationCode": "KMG"},
    {"stationName": "哈尔滨太平国际机场", "stationCode": "HRB"},
    {"stationName": "长春龙嘉国际机场", "stationCode": "CGQ"},
    {"stationName": "南昌昌北国际机场", "stationCode": "KHN"},
    {"stationName": "海口美兰国际机场", "stationCode": "HAK"},
    {"stationName": "三亚凤凰国际机场", "stationCode": "SYX"},
    {"stationName": "拉萨贡嘎国际机场", "stationCode": "LXA"},
    {"stationName": "乌鲁木齐地窝堡国际机场", "stationCode": "URC"},
    {"stationName": "西宁曹家堡国际机场", "stationCode": "XNN"},
    {"stationName": "银川河东国际机场", "stationCode": "INC"},
    {"stationName": "呼和浩特白塔国际机场", "stationCode": "HET"},
    {"stationName": "兰州中川国际机场", "stationCode": "LHW"},
]

flightCodes = {
    "CA" : "中国国际航空公司",
    "MU" : "中国东方航空公司",
    "CZ" : "中国南方航空公司",
    "3U" : "四川航空公司",
    "ZH" : "深圳航空公司",
    "GS" : "甘肃航空公司",
    "HU" : "海南航空公司",
    "JD" : "首都航空公司",
    "KN" : "中国联合航空公司",
    "MF" : "厦门航空公司",
}

""" [
    {
        flightId: 航班编号,
        flightCode: 航班代码,
        flightName: 航空公司名称,
        from: 始发地,
        to: 目的地,
        departTime: 出发时间,
        arriveTime: 到达时间,
        price: 价格,
        supportStudent: 是否支持学生票
    }
]
"""
flights = [
    # {"flightId": "1", "flightCode": "CA1234", "flightName": "中国国际航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "2", "flightCode": "MU2345", "flightName": "中国东方航空公司", "from": "上海浦东国际机场", "to": "广州白云国际机场", "departTime": "2021-09-01 12:00", "arriveTime": "2021-09-01 14:00", "price": "1200", "supportStudent": "true"},
    # {"flightId": "3", "flightCode": "CZ3456", "flightName": "中国南方航空公司", "from": "广州白云国际机场", "to": "深圳宝安国际机场", "departTime": "2021-09-01 16:00", "arriveTime": "2021-09-01 18:00", "price": "800", "supportStudent": "true"},
    # {"flightId": "4", "flightCode": "3U4567", "flightName": "四川航空公司", "from": "成都双流国际机场", "to": "重庆江北国际机场", "departTime": "2021-09-01 20:00", "arriveTime": "2021-09-01 22:00", "price": "600", "supportStudent": "true"},
    # {"flightId": "5", "flightCode": "ZH5678", "flightName": "深圳航空公司", "from": "深圳宝安国际机场", "to": "杭州萧山国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "6", "flightCode": "GS6789", "flightName": "甘肃航空公司", "from": "兰州中川国际机场", "to": "银川河东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "7", "flightCode": "HU7890", "flightName": "海南航空公司", "from": "海口美兰国际机场", "to": "三亚凤凰国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "8", "flightCode": "JD8901", "flightName": "首都航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "9", "flightCode": "KN9012", "flightName": "中国联合航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "10", "flightCode": "MF0123", "flightName": "厦门航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "11", "flightCode": "SC1234", "flightName": "山东航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "12", "flightCode": "CA1234", "flightName": "中国国际航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-01 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "13", "flightCode": "MU2345", "flightName": "中国东方航空公司", "from": "上海浦东国际机场", "to": "广州白云国际机场", "departTime": "2021-09-02 12:00", "arriveTime": "2021-09-01 14:00", "price": "1200", "supportStudent": "true"},
    # {"flightId": "14", "flightCode": "CZ3456", "flightName": "中国南方航空公司", "from": "广州白云国际机场", "to": "深圳宝安国际机场", "departTime": "2021-09-02 16:00", "arriveTime": "2021-09-01 18:00", "price": "800", "supportStudent": "true"},
    # {"flightId": "15", "flightCode": "3U4567", "flightName": "四川航空公司", "from": "成都双流国际机场", "to": "重庆江北国际机场", "departTime": "2021-09-02 20:00", "arriveTime": "2021-09-01 22:00", "price": "600", "supportStudent": "true"},
    # {"flightId": "16", "flightCode": "ZH5678", "flightName": "深圳航空公司", "from": "深圳宝安国际机场", "to": "杭州萧山国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "17", "flightCode": "GS6789", "flightName": "甘肃航空公司", "from": "兰州中川国际机场", "to": "银川河东国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "18", "flightCode": "HU7890", "flightName": "海南航空公司", "from": "海口美兰国际机场", "to": "三亚凤凰国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "19", "flightCode": "JD8901", "flightName": "首都航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "20", "flightCode": "KN9012", "flightName": "中国联合航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "21", "flightCode": "MF0123", "flightName": "厦门航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},
    # {"flightId": "22", "flightCode": "SC1234", "flightName": "山东航空公司", "from": "北京首都国际机场", "to": "上海浦东国际机场", "departTime": "2021-09-02 08:00", "arriveTime": "2021-09-01 10:00", "price": "1000", "supportStudent": "true"},

]

def stationNameAtSameCity(station1, station2):
    for i in range(len(stations)):
        if stations[i]["stationName"] == station1:
            for j in range(len(stations)):
                if stations[j]["stationName"] == station2 and stations[i]["stationName"] == stations[j]["stationName"]:
                    return True
    return False

def gen_flights():
    # 每天生成25-35个航班
    least = 50
    most = 100
    numDay = 5
    days = [random.randint(least, most) for i in range(numDay)]
    # 从今天开始，生成 numDay 天内的航班编号
    samplers = random.sample(range(1000, 9999), sum(days))
    for day in range(numDay):
        # 第day天的航班
        for i in range(days[day]):
            # 生成航班信息，随机生成
            departTime = datetime.datetime.now() + datetime.timedelta(days=day) + datetime.timedelta(hours=random.randint(0, 23)) + datetime.timedelta(minutes=random.randint(0, 59))
            arriveTime = departTime + datetime.timedelta(hours=random.randint(1, 5)) + datetime.timedelta(minutes=random.randint(0, 59))
            flightCode = random.choice(list(flightCodes.keys()))
            from_ = random.choice(stations)
            to_ = random.choice(stations)
            while to_["stationName"] == from_["stationName"]:
                to_ = random.choice(stations)
            flight = {
                "flightId": sum(days[:day]) + i,
                "flightCode": flightCode + str(samplers[sum(days[:day]) + i]),
                "flightName": flightCodes[flightCode],
                "from": from_["stationName"],
                "to": to_["stationName"],
                "departTime": departTime,
                "arriveTime": arriveTime,
                "price": random.randint(400, 1500),
                "ticketNum": random.randint(1, 100),
                "supportStudent": random.choice(["true", "false"])
            }
            flights.append(flight)

gen_flights()


avartas = [
    "https://img.freepik.com/premium-photo/3d-cartoon-man-flying-retro-airplane-isolated-image-cartoon-boy-is-riding-small-planes_524159-4266.jpg",
    "https://img.freepik.com/premium-vector/cute-air-hostess-hand-drawn-flat-stylish-cartoon-sticker-icon-concept-isolated-illustration_730620-1235047.jpg",
    "https://img.freepik.com/premium-vector/adorable-cartoon-icon-astronaut-operating-airplane_1263357-20603.jpg",
    "https://img.freepik.com/premium-vector/adorable-cartoon-icon-astronaut-operating-airplane_1263357-20603.jpg",
    "https://img.freepik.com/premium-vector/adorable-cartoon-icon-astronaut-operating-airplane_1263357-20603.jpg"
]

# {userId, orderId, sitNum, status, [flightId1, flightId2, ...]}
order = []

# 航班邻接表
graph = {}

# 航班邻接矩阵
arr = np.full((len(stations) + len(flights), len(stations) + len(flights)), float("inf"))
# for i in range(len(stations) + len(flights)):
    # arr.append([float("inf")] * (len(stations) + len(flights)))

# 二维数组，航班最短路径下一个结点（候选三个）
nexthop = np.full((len(stations) + len(flights), len(stations) + len(flights)), -1)

# 初始化邻接矩阵

# for i in range(len(flights)):
#     # nexthop.append([[-1,-1,-1]] * len(flights))
#     nexthop.append([-1] * len(flights))

# Dijkstra算法
def dijkstra(graph, start, end):
    def find_lowest_cost_node(costs):
        lowest_cost = float("inf")
        lowest_cost_node = None
        for node in costs:
            cost = costs[node]
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node
        return lowest_cost_node

    costs = {}
    parents = {}
    for node in graph:
        costs[node] = float("inf")
    costs[start] = 0
    parents[start] = None
    processed = []
    node = find_lowest_cost_node(costs)
    while node is not None:
        cost = costs[node]
        neighbors = graph[node]
        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            if n in costs and costs[n] > new_cost:
                costs[n] = new_cost
                parents[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs)

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path

# Floyd，从邻接矩阵计算最短路径
def floyd():
    # 从 flights 初始化 邻接表
    # 每个站点 stationCode 为一个结点
    # 每个航班 flightId 也为一个结点

    # 两个结点之间有向连接的条件：
    # 1.若两个结点是航班结点：两个航班的目的地和始发地相同 且 第一个航班的到达时间早于第二个航班的出发时间
    #   且有向连接的权重 = ( 第二个航班的出发时间 - 第一个航班的到达时间 ) * 第二个航班的价格 * 衔接时间因子
    # 2.若两个结点是站点结点：两个站点之间没有直接连接
    # 3.若源结点是站点结点，目标结点是航班结点：航班的始发地和站点相同
    #   且有向连接的权重 = ( 航班的到达时间 - 航班的出发时间 ) * 航班的价格
    # 4.若源结点是航班结点，目标结点是站点结点：航班的目的地和站点相同
    #   且有向连接的权重 = 0
    # 衔接时间因子是一个关于两个航班的时间差的函数，
    def connectTimeFactor(begin, end):
        # 时间差 < 40分钟 值在 2.0 - 3.0 之间
        # 时间差 < 1.5小时 值在 1.0 - 1.5 之间
        # 1小时 <= 时间差 < 2小时 值为 1.0
        # 2小时以上 值在 1.0 - 2.0 之间
        # 如果end早于begin，返回无穷大
        if end < begin:
            return float("inf")
        delta = (end - begin).seconds / 3600.0
        if delta < 0.7:
            return 2.0 + 1.0 * (0.7 - delta) / 0.7
        elif delta < 1.5:
            return 1.0 + 0.5 * (1.5 - delta) / 1.5
        elif delta < 2:
            return 1.0
        else:
            return 1.0 + 1.0 * (delta - 2.0)


    # 站点
    for i in range(len(stations)):
        for j in range(len(stations)):
            # TODO: 若城市名称相同，则权值也为0（暂时用不到）
            if i == j: # or stationNameAtSameCity(stations[i]["stationName"], stations[j]["stationName"]):
                arr[i,j] = 0
            else:
                arr[i,j] = float("inf")
    # 航班
    for i in range(len(stations), len(stations) + len(flights)):
        for j in range(len(stations), len(stations) + len(flights)):
            k = i - len(stations)
            l = j - len(stations)
            if flights[k]["to"] == flights[l]["from"] and flights[k]["arriveTime"] < flights[l]["departTime"]:
                # graph[i] = {j: (flights[l]["departTime"] - flights[k]["arriveTime"]).seconds/60 * flights[l]["price"] * connectTimeFactor(flights[k]["arriveTime"], flights[l]["departTime"])}
                arr[i, j] = abs((flights[l]["departTime"] - flights[k]["arriveTime"]).seconds/60) * flights[l]["price"] * connectTimeFactor(flights[k]["arriveTime"], flights[l]["departTime"])
                # arr[i, j] = flights[l]["price"]

    # 站点到航班
    for i in range(len(stations)):
        for j in range(len(stations), len(stations) + len(flights)):
            l = j - len(stations)
            if stations[i]["stationName"] == flights[l]["from"]:
                # graph[i] = {j: (flights[l]["arriveTime"] - flights[l]["departTime"]).seconds/60 * flights[l]["price"]}
                arr[i, j] = abs((flights[l]["arriveTime"] - flights[l]["departTime"]).seconds/60) * \
                    flights[l]["price"] * connectTimeFactor(
                        flights[l]["departTime"], flights[l]["arriveTime"])
                # arr[i, j] = flights[l]["price"]
    # 航班到站点
    for i in range(len(stations), len(stations) + len(flights)):
        for j in range(len(stations)):
            k = i - len(stations)
            if flights[k]["to"] == stations[j]["stationName"]:
                # graph[i] = {j: 0}
                arr[i,j] = 0

    temp = []
    # Floyd算法
    for k in range(len(flights)):   # 中间结点
        # if (k % 10 == 0):
        print("Floyding: {} / {}".format(k, len(flights)))
        for i in range(len(stations) + len(flights)):   # 起始结点
            for j in range(len(stations) + len(flights)):   # 终止结点
                if arr[i,j] > arr[i,k] + arr[k,j]:
                    arr[i,j] = arr[i,k] + arr[k,j]
                    # nexthop 存储三个候选结点，滚动更新
                    # temp = nexthop[i][j]
                    nexthop[i,j] = k #[k, temp[0], temp[1]]

floyd()


# 以下是接口定义
@app.api_route("/", methods=["GET", "POST", "OPTIONS"])
async def read_root():
    """Route to get root

    Returns:
        _type_: _description_
    """
    return "The Rat Tap Your Head! You are lost!"


# 查询站点
@app.api_route("/api/v1/queryStation", methods=["GET", "POST", "OPTIONS"])
async def query_station(request: Request):
    """由地名模糊查询站点名称

    Args:
        dishId (int): _description_

    Returns:
        _type_: _description_
    """

    """返回数据格式
    stationName | Array[stationName]
    """

    ret = []
    querys = request.query_params.get("stationName")
    if not querys:
        # 返回所有地名
        return JSONResponse(jsonable_encoder(stations))
    
    querys = jieba.lcut(querys)

    # 去除 带有 "机场"、"国际" 的元素
    for i in range(len(querys)):
        if "机场" in querys[i] or "国际" in querys[i]:
            querys[i] = ""

    for i in range(len(stations)):
        for j in range(len(querys)):
            if querys[j] and querys[j] in stations[i]["stationName"] and stations[i] not in ret:
                ret.append(stations[i])
                break

    return JSONResponse(jsonable_encoder(ret))


# 查询航班
@app.api_route("/api/v1/queryFlight", methods=["GET", "POST", "OPTIONS"])
async def query_flight(request: Request):
    """Route to query sit

    Returns:
        _type_: _description_
查询参数表:
date | Date(日期格式"2020-10-1") | 可选参数
from | string | 可选参数
to | string | 可选参数

返回值 (JSON Array):
flightCode | string (航班编号，2位公司英文编号+4位数字序列号)
flightName | string (班次名称)
supportStudent | Boolean (是否支持学生票)
price | number (价格)
from | string (始发地，模糊查找)
to | string (目的地，模糊查找)
info | string (描述)
num | number (剩余票数)
avatar | string (图像路径)
    """
    
    date = request.query_params.get("date")
    from_ = request.query_params.get("from")
    to = request.query_params.get("to")

    # 查询，从json提取站名数据
    froms = []
    tos = []

    if not from_:
        from_ = ""
    querys = jieba.lcut(from_)
    # 去除 带有 "机场"、"国际" 的元素
    for i in range(len(querys)):
        if "机场" in querys[i] or "国际" in querys[i]:
            querys[i] = ""

    for i in range(len(stations)):
        for j in range(len(querys)):
            if querys[j] and querys[j] in stations[i]["stationName"] and stations[i] not in froms:
                froms.append(stations[i])
                break

    if not to:
        to = ""
    querys = jieba.lcut(to)
    # 去除 带有 "机场"、"国际" 的元素
    for i in range(len(querys)):
        for j in "机场国际".split():
            if j in querys[i]:
                querys[i] = ""

    for i in range(len(stations)):
        for j in range(len(querys)):
            if querys[j] and querys[j] in stations[i]["stationName"] and stations[i] not in tos:
                tos.append(stations[i])
                break

    ret = []
    if len(froms) == 0 and len(tos) == 0:
        # 通过日期查询
        # 查询当天航班
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            today = True
        for i in range(len(flights)):
            # departTime是一个包含时分秒的日期
            if flights[i]["departTime"].strftime("%Y-%m-%d") == date:
                ret.append(flights[i])
    else:
        # TODO: 一个城市一般只有一个机场，所以只取第一个
        if len(froms):
            from_ = froms[0].get("stationName")
        else:
            from_ = ""
        if len(tos):
            to = tos[0].get("stationName")
        else:
            to = ""
        for i in range(len(flights)):
            if (not from_ or from_ == flights[i]["from"]) and (not to or to == flights[i]["to"]):
                ret.append({
                    "flightCode": flights[i]["flightCode"],
                    "flightName": flights[i]["flightName"],
                    "supportStudent": flights[i]["supportStudent"],
                    "price": flights[i]["price"],
                    "from": flights[i]["from"],
                    "to": flights[i]["to"],
                    "info": "{}航班从{}飞往{}价格{}元".format(flights[i]["flightId"], flights[i]["from"], flights[i]["to"], flights[i]["price"]),
                    "num": flights[i]["ticketNum"],
                    "avatar": random.choice(avartas)
                })
    
    return JSONResponse(jsonable_encoder(ret))
    
# 制定行程计划
@app.api_route("/api/v1/plan", methods=["GET", "POST", "OPTIONS"])
async def plan(request: Request):
    """Route to plan

    Args:
        plan (List[dict]): _description_

    Returns:
        _type_: _description_

** Arguments:
date | Date(日期格式"2020-10-1") | 可选参数
from | string | 可选参数（from和to不能只填一个，不然只根据日期查询）
to | string | 可选参数（from和to不能只填一个，不然只根据日期查询）

** Returns (JSON Array):
flights | Array[flight] (航班对象数组)
** Each element include in `flights` are sequential:
flightId | number (航班编号，请务必记住航班对应的该编号，用于后面提交订单时使用)
flightCode | string (航班编号，2位公司英文编号+4位数字序列号)
price | number (价格)
from | string (始发地，模糊查找)
to | string (目的地，模糊查找)
num | number (剩余票数)
avatar | string (图像路径)
"""
    date = request.query_params.get("date")
    from_ = request.query_params.get("from")
    to = request.query_params.get("to")
    
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if not from_ or not to:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "查询失败，需要完整的始发地和目的地参数"}))

    # 查询，从json提取站名数据
    froms = []
    tos = []

    querys = jieba.lcut(from_)
    # 去除 带有 "机场"、"国际" 的元素
    for i in range(len(querys)):
        if "机场" in querys[i] or "国际" in querys[i]:
            querys[i] = ""

    for i in range(len(stations)):
        for j in range(len(querys)):
            if querys[j] and querys[j] in stations[i]["stationName"] and stations[i] not in froms:
                froms.append(stations[i])
                break

    querys = jieba.lcut(to)
    # 去除 带有 "机场"、"国际" 的元素
    for i in range(len(querys)):
        if "机场" in querys[i] or "国际" in querys[i]:
            querys[i] = ""

    for i in range(len(stations)):
        for j in range(len(querys)):
            if querys[j] and querys[j] in stations[i]["stationName"] and stations[i] not in tos:
                tos.append(stations[i])
                break

    if len(froms) == 0 or len(tos) == 0:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "查询失败，始发地和目的地为空"}))
    
    # TODO: 一个城市一般只有一个机场，所以只取第一个

    from_ = froms[0].get("stationName")
    to = tos[0].get("stationName")
    fromi = stations.index(froms[0])
    toi = stations.index(tos[0])


    # 使用 arr 和 nexthop 数组 查询最优路径
    # arr 是 i, j 全局最优价格的 邻接矩阵，nexthop 是从 i 到 j 下一个结点的最优站点，包含三个候选
    # ret: [{flights: [flight1, flight2, ...]}, cost: 价格]
    ret = []
    path = []
    # 
    node = toi
    path.append(stations[node])

    cost = 0
    # nexthop[i,j]存储i到j的最后一个最优点，所以从to开始找
    while node != fromi:
        nextnode = nexthop[fromi, node]
        if nextnode == -1 or toi == node and flights[nextnode - len(stations)]["to"] != stations[node]["stationName"]:
            break
        if nextnode < len(stations):
            path.insert(0, stations[nextnode])
        else:
            path.insert(0, flights[nextnode - len(stations)])
            cost += flights[nextnode - len(stations)]['price']
        node = nextnode
        
    
    if path[0] and ("stationName" in path[0] and (path[0]["stationName"] == fromi)):
        ret.append({"flights": path, "cost": cost})
    elif path[0] and ("from" in path[0] and (path[0]["from"] == from_)):
        ret.append({"flights": path, "cost": cost})

    return JSONResponse(jsonable_encoder(ret))

# 提交订单
@app.api_route("/api/v1/appendOrder", methods=["GET", "POST", "OPTIONS"])
async def append_order(request: Request):
    """Route to append order

    Args:
        order (List[dict]): _description_

    Returns:
        _type_: _description_
    
** 查询参数表:
userId | number (用户编号) | 必填
flightsId | Array[flightId] (航班编号数组) | 必填

** 返回值 (JSON object):
status | "true" 如果成功 "false" 如果失败
msg | string (订单结果描述)
price | number (订单价格)
orderId | string (订单编号)
imgUrl | string (支付付款码地址)
msg | string (订单描述)
    """
    sitNum = request.query_params.get("sitNum")
    userId = request.query_params.get("userId")
    flightsId = request.query_params.get("flightsId")

    if not userId or not flightsId:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，需要用户Id、航班Id参数"}))
    
    userId = ast.literal_eval(userId)
    flightsId = ast.literal_eval(flightsId)

    if not isinstance(flightsId, list) or not isinstance(userId, int):
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，参数类型错误"}))
    
    if not isinstance(flightsId, list):
        flightsId = [flightsId,]

    if len(flightsId) == 0:
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，航班为空"}))
    
    price = 0
    for i in range(len(flightsId)):
        # 从flights中查找flightId
        if int(flightsId[i]) < 1 or flightsId[i] > len(flights):
            return JSONResponse(jsonable_encoder({"status": "false", "msg": "提交订单失败，找不到航班:flightId:{}".format(flightsId[i])}))
        price += flights[int(flightsId[i])]["price"] * sitNum

    orderId = random.randint(100000, 999999)
    imgUrl = "https://www.baidu.com"
    order.append({"userId": userId, "orderId": orderId, "sitNum": sitNum, "flights": flights})
    return JSONResponse(jsonable_encoder({"status": "true", "msg": "提交订单成功", "price": price, "orderId": orderId, "imgUrl": imgUrl}))


# 获取订单信息
@app.api_route("/api/v1/get_desk_form")
async def get_desk_form(request: Request):
    """ Route to retrieve order information 
    
    Returns:
        [
            {
                orderId: 订单编号,
                
                items: [
                    name: 航班名称,
                    desc: 航班描述,
                    image: 航班图像,
                ]
            }
        ]
    """

    print(request.query_params)

    userId = request.query_params.get("userId")
    userId = ast.literal_eval(userId)

    if not isinstance(userId, int):
        return JSONResponse(jsonable_encoder({"status": "false", "msg": "获取订单失败，需要用户Id参数"}))

    ret = []
    for i in range(len(order)):
        if order[i]["userId"] == userId:
            items = []
            for j in range(len(order[i]["flights"])):
                flight = flights[order[i]["flights"][j]-1]
                items.append(
                    {"name": flight["flightCode"], "desc": "航空公司: " + flight["flightName"] + "，方向:从" + flight["from"] + " 到 " + flight["to"] + ", 时间: " + flight["departTime"] + ", 票价: " + flight["price"], "image": random.choice(avartas)})
            ret.append({"orderId": order[i]["orderId"], "items": items})
    return JSONResponse(jsonable_encoder(ret))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
