# from langchain.vectorstores import Chroma
from bson import ObjectId
from langchain.chains import ConversationalRetrievalChain
# from langchain.chat_models import ChatOpenAI
from langchain.chains.conversational_retrieval.base import _get_chat_history
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts.prompt import PromptTemplate

from qa_chain.MyAPIChain.MyAPIChain import MyAPIChain
from qa_chain.model_to_llm import model_to_llm
from qa_chain.get_vectordb import get_vectordb


class Chat_QA_chain_self:
    """"
    带历史记录的问答链  
    - model：调用的模型名称
    - temperature：温度系数，控制生成的随机性
    - top_k：返回检索的前k个相似文档
    - chat_history：历史记录，输入一个列表，默认是一个空列表
    - history_len：控制保留的最近 history_len 次对话
    - file_path：建库文件所在路径
    - persist_path：向量数据库持久化路径
    - appid：星火
    - api_key：星火、百度文心、OpenAI、智谱都需要传递的参数
    - Spark_api_secret：星火秘钥
    - Wenxin_secret_key：文心秘钥
    - embeddings：使用的embedding模型
    - embedding_key：使用的embedding模型的秘钥（智谱或者OpenAI）  
    """
    def __init__(self,model:str, temperature:float=0.0, top_k:int=4, chat_history:list=[], file_path:str=None, persist_path:str=None, appid:str=None, api_key:str=None, Spark_api_secret:str=None,Wenxin_secret_key:str=None, embedding = "openai",embedding_key:str=None, template=None, API_DOC=None):
        self.model = model
        self.temperature = temperature
        self.top_k = top_k
        self.chat_history = chat_history
        #self.history_len = history_len
        self.file_path = file_path
        self.persist_path = persist_path
        self.appid = appid
        self.api_key = api_key
        self.Spark_api_secret = Spark_api_secret
        self.Wenxin_secret_key = Wenxin_secret_key
        self.embedding = embedding
        self.embedding_key = embedding_key
        self.template = template
        self.API_DOC = API_DOC
        self.chat_start_index: int = None


        self.vectordb = get_vectordb(self.file_path, self.persist_path, self.embedding,self.embedding_key)
        
    
    def clear_history(self):
        "清空历史记录"
        return self.chat_history.clear()

    
    def change_history_length(self,history_len:int=1):
        """
        保存指定对话轮次的历史记录
        输入参数：
        - history_len ：控制保留的最近 history_len 次对话
        - chat_history：当前的历史对话记录
        输出：返回最近 history_len 次对话
        """
        n = len(self.chat_history)
        return self.chat_history[n-history_len:]

 
    def answer(self, question:str=None,temperature = None, top_k = 4, **kwargs):
        """"
        核心方法，调用问答链
        arguments: 
        - question：用户提问
        """
        
        if len(question) == 0:
            return "", self.chat_history
        
        if len(question) == 0:
            return ""
        
        if temperature == None:
            temperature = self.temperature

        llm = model_to_llm(self.model, temperature, self.appid, self.api_key, self.Spark_api_secret,self.Wenxin_secret_key)

        # 深度理解链
        deepkTemplateStr = """Given the chat history below, please answer the question in short as possible:
** Chat history:
{chat_history}

** User Question:
{question}

** What is the purpose of the user now?
Your Answer:
"""
        deepkTemplate = PromptTemplate(template=deepkTemplateStr, input_variables=[
                "chat_history", "question"])
        deepkTemplate.partial(chat_history=_get_chat_history(self.chat_history), question=question)
        deepkChain = LLMChain(llm=llm, prompt=deepkTemplate,
                              output_key="question_nested")

        #self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        
        # APIChain
        api_chain = MyAPIChain.from_llm_and_api_docs(llm,
                verbose=True,       # Debug mode
                question_key="question_nested",
                output_key="api_response",
                api_docs=self.API_DOC,  # headers=headers,
                userId=kwargs.get("userId", 253),
                limit_to_domains=["http://127.0.0.1:3000/"],
                )
        
        # ConversationalRetrievalChain
        retriever = self.vectordb.as_retriever(search_type="similarity",
                                            search_kwargs={'k': top_k})  # 默认similarity，k=4
        messages = [
            SystemMessagePromptTemplate.from_template(self.template),
            HumanMessagePromptTemplate.from_template(question)
        ]
        qa_prompt = ChatPromptTemplate(input_variables=["api_response", "question", "chat_history", "context"],
            messages=messages)
        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm = llm,
            retriever = retriever,
            #kwargs={"prompt": self.template}
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )

        # 阅读理解链、API链、对话链
        overall_chain = SequentialChain(
            chains=[deepkChain, api_chain, conversational_chain],
            input_variables=["question", "chat_history"],
            output_variables=["api_response", "answer"],
            verbose=True)

        # Run
        result = overall_chain({
            "context": " ",
            "question": question,
            "chat_history": self.chat_history})
        
        answer =  result['answer']

        self.chat_history.append((question,answer)) #更新历史记录

        return self.chat_history  #返回本次回答和更新后的历史记录
