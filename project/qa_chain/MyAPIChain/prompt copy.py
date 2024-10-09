# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

API_URL_PROMPT_TEMPLATE = """你是一个API生成程序，解决用户的问题，你需要决定是否生成一个URL解决用户的问题。
下面请阅读API文档

{api_docs}

**要求
1.你需要获取到回答问题所需的信息，并决定是否生成一个尽可能简短的URL。请注意如果需要生成时，在回答中刻意排除任何不必要的数据
2.如果你已经解决完用户的问题，请在回答的最后下一行中填入`完成`标记，不要填其他内容
3.用户已知内容包含你需要的内容，请仔细检查，如果用户已知的内容已经可以解决问题，你不需要生成URL，在回答的最后下一行中填入`完成`标记。
4.聊天历史包含语境所需要的信息，请仔细理解
5.如果需要的参数你不知道，说明你不能一次性解决用户的问题，这时你只需要生成URL用于获取这个参数
6.你回答的内容除了URL、完成标记外，不要包含其他内容

**用户的问题:
{question}

**用户已知内容:
{context}

**聊天历史:
{chat_history}

**Your Answer:"""

API_URL_PROMPT = PromptTemplate(
    input_variables=[
        "api_docs",
        "question",
        "context",
        "chat_history",
    ],
    template=API_URL_PROMPT_TEMPLATE,
)

# API_RESPONSE_PROMPT_TEMPLATE = (
#     API_URL_PROMPT_TEMPLATE
#     + """ {api_url}

# Here is the response from the API:

# {api_response}

# Summarize this response to answer the original question.

# Summary:"""
# )

# API_RESPONSE_PROMPT = PromptTemplate(
#     input_variables=["api_docs", "question",
#                      "api_url", "api_response"],
#     template=API_RESPONSE_PROMPT_TEMPLATE,
# )
