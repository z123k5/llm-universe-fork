from itertools import chain
import os, sys
import redis
from ConnectionPool import assistants_collection, service_desk_collection
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from pydantic import BaseModel
# 导入功能模块目录
sys.path.append("../")
from qa_chain.Chat_QA_chain_self import Chat_QA_chain_self


chainpoll = {}


# 定义一个数据模型，用于接收POST请求中的数据
class Item(BaseModel):
    model : str = "gpt-3.5-turbo"# 使用的模型
    temperature : float = 0.1# 温度系数
    history_len : int = 10 # 是否使用历史对话功能
    # API_Key
    api_key: str = None
    # access_token
    access_token: str = None
    # APPID（星火）
    appid : str = None
    # APISecret
    Spark_api_secret : str = None
    # Secret_key
    Wenxin_secret_key : str = None
    # 数据库路径
    db_path : str = "../../data_base/data_base/vector_db/chroma"
    # 源文件路径
    file_path : str = "../../data_base/data_base/knowledge_db"
    # prompt template
    prompt_template : str = None
    # Template 变量
    input_variables : list = ["context","question"]
    # Embdding
    embedding : str = "openai"
    # Top K
    top_k : int = 5
    # embedding_key
    embedding_key : str = None

class ChatConfig(Item):
    appname : str = None
    API_DOC : str = None

class ChatPool:
    def openchat(self, username: str, config: ChatConfig):
        if chainpoll.get(username+'-'+config.appname):
            return True
        assistant = assistants_collection.find_one({"name": config.appname})
        service_desk = service_desk_collection.find_one({"name": config.appname})
        if not assistant :
            return False
        
        prompt_template = None
        api_doc = None
        # Read prompt template from file
        with open(os.getenv('RES_DIR') + assistant.get("promptEngineeringLibrary").get("path"), 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        with open(os.getenv('RES_DIR') + service_desk.get("apiDocuments").get("path"), 'r', encoding='utf-8') as f:
            api_doc = f.read()
        
        config.file_path = os.getenv('RES_DIR')+assistant.get("corpus").get("path")
        config.db_path = os.getenv('RES_DIR')+assistant.get("behaviorLibrary").get("path")
        config.prompt_template = prompt_template
        config.API_DOC = api_doc
        
        chain = Chat_QA_chain_self(model=config.model, temperature=config.temperature, file_path=config.file_path, persist_path=config.db_path, appid=config.appid, api_key=config.api_key, Spark_api_secret=config.Spark_api_secret, Wenxin_secret_key=config.Wenxin_secret_key, embedding=config.embedding, embedding_key=config.embedding_key, template=config.prompt_template, API_DOC=config.API_DOC)
        chainpoll[username+'-'+config.appname] = chain
        return True
    
    def chat_text(self, username, appname, prompt):
        chain = chainpoll.get(username+'-'+appname)
        if not chain:
            raise ValueError("Chat chain is not open")
        response = chain.answer(question = prompt)
        return response
    
    # Experimental
    def chat_audio(self, username, appname, audio):
        chain = chainpoll.get(username+'-'+appname)
        if not chain:
            raise ValueError("Chat chain is not open")
        response = chain.answer(question = audio)
        return response
    
    def get_history(self, username):
        return chain.chat_history

chatpoll = ChatPool()
