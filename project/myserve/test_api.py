# import openai

# # 设置API密钥
# openai.api_key = "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"

# # 发送请求到OpenAI API
# response = openai.Completion.create(
#     engine="gpt-3.5-turbo",
#     prompt="你好，世界！",
#     max_tokens=50
# )

# # 打印响应
# print(response.choices[0].text.strip())

from zhipuai import ZhipuAI
client = ZhipuAI(api_key="0bb21fde0006bb1904ef42c5aaf07876.i6nkUMEbMjb9X7Em") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
    ],
)
print(response.choices[0].message)