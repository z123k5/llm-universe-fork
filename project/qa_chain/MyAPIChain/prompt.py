# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

API_URL_PROMPT_TEMPLATE = """You are given the below API Documentation:
{api_docs}
Following the 6 steps below to generate the full API url to call for answering the user question:
1. (Important)You should build the API url in order to get a response that is as short as possible, while still getting the necessary information to answer the question. Pay attention to deliberately exclude any unnecessary pieces of data in the API call.
2. Using this documentation, generate the full API url to call for answering the user question.
3. If the API arguments you want isn't present in Prerequisites, you should think which full API url to generate first.
4. Pay attention to refer the latest Prerequisites.
5. If the Prerequisites shows some error msg, don't generate the API url, mark 'done' in answer end.
6. If the Prerequisites already satisfied user's question, don't generate the API url, mark 'done' in answer end.

Prerequisites:
{context}

Question:{question}
Your Answer(Pay attention to deliberately exclude any unnecessary pieces of data, as short as possible):"""

API_URL_PROMPT = PromptTemplate(
    input_variables=[
        "api_docs",
        "question",
        "context",
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
