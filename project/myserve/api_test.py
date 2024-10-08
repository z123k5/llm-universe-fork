import requests
import json

url = "https://chatapi.midjourney-vip.cn/v1/chat/completions"

payload = json.dumps({
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": """'You are given the below API Documentation:\nAPI 文档:\n目标: http://127.0.0.1:3000\n\n1. 查询菜单，需要查看本店的所有菜品时调用\n(GET) http://127.0.0.1:3000/api/v1/menu\n查询参数表:\nNone\n返回值 (JSON object):\ndishes | array[dish] (菜品对象)\n\n在 dish 对象中包含下列值\ndishId | string (菜品编号) \nname | string (菜品名称)\nprice | string (价格)\ninfo | string (描述)\navatar | string (图像路径)\n\n2. 发起订单\n(POST) http://127.0.0.1:3000/api/v1/appendOrder\n查询参数表:\ndishId | array[string] (菜品编号数组) | 必须\nname | array[string] (菜品名称数组) | 必须\n返回值 (JSON object):\nstatus | "true" 如果成功 "false" 如果失败\nmsg | string (订单结果描述)\n\n3. 查询空闲座位数量\n(GET) http://127.0.0.1:3000/api/v1/querySit\n查询参数表:\nNone\n返回值 (JSON object):\nnum | string (空闲座位数量)\nmsg | string (结果描述)\n\nUsing this documentation, generate the full API url to call for answering the user question.\nYou should build the API url in order to get a response that is as short as possible, while still getting the necessary information to answer the question. \n\nQuestion:how much dishes of the responce in?\nAPI url: http://127.0.0.1:3000/api/v1/menu\n\nHere is the response from the API:\n\n[
    {
        "dishId": "1",
        "name": "鱼香肉丝",
        "price": "20",
        "info": "鱼香肉丝是一道传统川菜，属于川菜系，是一道以猪肉丝为主要食材制作而成的川菜。",
        "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    },
    {
        "dishId": "2",
        "name": "宫保鸡丁",
        "price": "25",
        "info": "宫保鸡丁是一道传统川菜，属于川菜系，是一道以鸡肉丁为主要食材制作而成的川菜。",
        "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    },
    {
        "dishId": "3",
        "name": "地三鲜",
        "price": "18",
        "info": "地三鲜是一道传统东北菜，属于东北菜系，是一道以茄子、土豆、青椒为主要食材制作而成的东北菜。",
        "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    },
    {
        "dishId": "4",
        "name": "红烧肉",
        "price": "30",
        "info": "红烧肉是一道传统川菜，属于川菜系，是一道以猪肉为主要食材制作而成的川菜。",
        "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    },
    {
        "dishId": "5",
        "name": "酸辣土豆丝",
        "price": "15",
        "info": "酸辣土豆丝是一道传统川菜，属于川菜系，是一道以土豆丝为主要食材制作而成的川菜。",
        "avatar": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    }
]\n\nSummarize this response to answer the original question.\n\nSummary:'"""},
    ],
})
headers = {
    'X-OpenAI-Client-User-Agent': '{"bindings_version": "0.27.6", "httplib": "requests", "lang": "python", "lang_version": "3.10.11", "platform": "Windows-10-10.0.22631-SP0", "publisher": "openai", "uname": "Windows 10 10.0.22631 AMD64 Intel64 Family 6 Model 158 Stepping 10, GenuineIntel"}',
    # 'Accept': 'application/json',
    # 'xxx' is your API key, 换成你的令牌
    'Authorization': 'Bearer sk-q5BPovxzZqSdiCN86029880a492b4e579dB4F66e8dC503Af',
    'User-Agent': 'OpenAI/v1 PythonBindings/0.27.6',
    'Content-Type': 'application/json'
}
# payload = json.dumps({
#     "model": "gpt-4",
#     "messages": [
#         {"role": "system", "content": "你是年轻人,批判现实,思考深刻,语言风趣,只输出SVG格式内的内容"},
#         {"role": "user", "content": '''
# # Role: 汉语新解
# - **Profile:**
# - **Description:** 以独特视角解析汉语词汇，运用批判性思维与讽刺幽默，风格融合Oscar Wilde、鲁迅、林语堂，特点包括一针见血、深刻隐喻、辛辣讽刺。目标是通过简洁有力的表达，提供创新性的汉语词汇解释，帮助用户获得更深的理解。

# - **Goals:**
#   - **一句话描述:** 根据用户输入的汉语词汇，生成新颖、独特的解释，助用户全面透析其含义。

# - **Constraints:**
#   - 解释需简练犀利，突出本质，结合隐喻、讽刺和幽默，不失优雅。
#   - 避免长篇大论，表达风格需简洁。

# - **Skills:**
#   - 独特视角
#   - 批判性思维
#   - 幽默与讽刺
#   - 精准隐喻
#   - 一针见血的表达

# - **Style:**
#   - **核心风格:** 以辛辣讽刺为刀锋，配以优雅的隐喻，直指词汇背后的真相。
#   - **表达特征:** 像在刀刃上撒糖，一边温柔安抚，一边揭穿表象。

# - **Workflow:**
#   1. **用户输入的词语是【生日快乐】**。
#   2. **结合Oscar Wilde、鲁迅、林语堂的风格**，通过隐喻、讽刺、幽默解构词汇含义。
#   3. **输出格式**为：
#     <svg width="400" height="500" xmlns="http://www.w3.org/2000/svg">
#  <style>
#    .background { fill: #F1EAD7; }
#    .title { font: 24px '毛笔楷体'; fill: #333; text-anchor: middle; }
#    .text { font: 16px '汇文明朝体'; fill: #666; text-anchor: middle; }
#    .word { font: 20px '毛笔楷体'; fill: #333; text-anchor: middle; }
#    .line { stroke: #333; stroke-width: 2; }
#  </style>
#  <rect width="100%" height="100%" class="background" />
#  <text x="50%" y="50" class="title">汉语新解</text>
#  <line x1="20" y1="70" x2="380" y2="70" class="line" />
#  <text x="50%" y="100" class="word">用户输入的词语</text>
#  <text x="50%" y="130" class="text">用户词语的拼音</text>
#  <text x="50%" y="160" class="text">
#    <tspan x="50%" dy="20">输出词语的解释（以讽刺隐喻切入，简练点出词汇的核心）</tspan>
#  </text>
# </svg>
# '''
#          },
#     ],
# })

headers = {
    'X-OpenAI-Client-User-Agent': '{"bindings_version": "0.27.6", "httplib": "requests", "lang": "python", "lang_version": "3.10.11", "platform": "Windows-10-10.0.22631-SP0", "publisher": "openai", "uname": "Windows 10 10.0.22631 AMD64 Intel64 Family 6 Model 158 Stepping 10, GenuineIntel"}',
    # 'Accept': 'application/json',
    # 'xxx' is your API key, 换成你的令牌
    'Authorization': 'Bearer sk-q5BPovxzZqSdiCN86029880a492b4e579dB4F66e8dC503Af',
    'User-Agent': 'OpenAI/v1 PythonBindings/0.27.6',
    'Content-Type': 'application/json'
}

# 使用 requests.Session
session = requests.Session()
response = requests.post(url, headers=headers, data=payload)

print(response.text)
