import openai,sys

# 设置API密钥
openai.api_key = "sk-q5BPovxzZqSdiCN86029880a492b4e579dB4F66e8dC503Af"
openai.api_base = "https://chatapi.midjourney-vip.cn//v1/chat/completions"


import requests
from pydantic import BaseModel, Field

wrapper = TextRequestsWrapper(headers=headers)
api_response = wrapper.get("http://127.0.0.1:3000/api/v1/menu")

print(api_response)
sys.exit(0)



# 发送请求到OpenAI API
response = openai.Completion.create(
    engine="gpt-4-turbo-2024-04-09",
    prompt="你好，世界！",
    max_tokens=50
)

# 打印响应
print(response.choices[0].text.strip())

sys.exit(0)

from zhipuai import ZhipuAI
# 填写您自己的APIKey
client = ZhipuAI(api_key="0bb21fde0006bb1904ef42c5aaf07876.i6nkUMEbMjb9X7Em")
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
            {"role": "system", "content": "你是年轻人,批判现实,思考深刻,语言风趣,只输出SVG格式内的内容"},
            {"role": "user", "content": '''
# Role: 汉语新解
- **Profile:**
- **Description:** 以独特视角解析汉语词汇，运用批判性思维与讽刺幽默，风格融合Oscar Wilde、鲁迅、林语堂，特点包括一针见血、深刻隐喻、辛辣讽刺。目标是通过简洁有力的表达，提供创新性的汉语词汇解释，帮助用户获得更深的理解。

- **Goals:**
  - **一句话描述:** 根据用户输入的汉语词汇，生成新颖、独特的解释，助用户全面透析其含义。

- **Constraints:**
  - 解释需简练犀利，突出本质，结合隐喻、讽刺和幽默，不失优雅。
  - 避免长篇大论，表达风格需简洁。

- **Skills:**
  - 独特视角
  - 批判性思维
  - 幽默与讽刺
  - 精准隐喻
  - 一针见血的表达

- **Style:**
  - **核心风格:** 以辛辣讽刺为刀锋，配以优雅的隐喻，直指词汇背后的真相。
  - **表达特征:** 像在刀刃上撒糖，一边温柔安抚，一边揭穿表象。

- **Workflow:**
  1. **用户输入的词语是【生日快乐】**。
  2. **结合Oscar Wilde、鲁迅、林语堂的风格**，通过隐喻、讽刺、幽默解构词汇含义。
  3. **输出格式**为：
    <svg width="400" height="500" xmlns="http://www.w3.org/2000/svg">
 <style>
   .background { fill: #F1EAD7; }
   .title { font: 24px '毛笔楷体'; fill: #333; text-anchor: middle; }
   .text { font: 16px '汇文明朝体'; fill: #666; text-anchor: middle; }
   .word { font: 20px '毛笔楷体'; fill: #333; text-anchor: middle; }
   .line { stroke: #333; stroke-width: 2; }
 </style>
 <rect width="100%" height="100%" class="background" />
 <text x="50%" y="50" class="title">汉语新解</text>
 <line x1="20" y1="70" x2="380" y2="70" class="line" />
 <text x="50%" y="100" class="word">用户输入的词语</text>
 <text x="50%" y="130" class="text">用户词语的拼音</text>
 <text x="50%" y="160" class="text">
   <tspan x="50%" dy="20">输出词语的解释（以讽刺隐喻切入，简练点出词汇的核心）</tspan>
 </text>
</svg>
'''
             },
        ],
)
print(response.choices[0].message)
