import hashlib
from itertools import chain
import os, sys

import requests
from bson import ObjectId
import redis
import uuid
from ConnectionPool import assistants_collection, service_desk_collection, messages_collection
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
    def get_objid(self, string):
        hash_object = hashlib.sha256(string.encode())
        hash_hex = hash_object.hexdigest()
        return ObjectId(hash_hex[:24])

    def get_objid_int8(self, string):
        hash_object = hashlib.sha256(string.encode())
        hash_hex = hash_object.hexdigest()
        # range from 0 to 1024
        return int(hash_hex[:2], base=16)
    
    def clear_history(self, username, appname=None):
        # Clear all chat history
        messages_collection.delete_many({"senderId": self.get_objid(username), "receiverId": self.get_objid(appname)})
        messages_collection.delete_many({"senderId": self.get_objid(appname), "receiverId": self.get_objid(username)})
        return True

    def save_history(self, username, appname, history, last_index):
        """Format
        [
            [
            "User dialogue",
            "Assistant dialogue",
            ],
            [
            "User dialogue",
            "Assistant dialogue",
            ],
            ...
        ]
        """
        schema = []
        chat_id = self.get_objid(username+'-'+appname)
        sender_id = self.get_objid(username)
        receiver_id = self.get_objid(appname)
        for i in range(int(last_index/2), len(history)):
            schema.append(
                {
                    "chatId": chat_id,
                    "senderId": sender_id,
                    "receiverId": receiver_id,
                    "messageType": "text", 
                    "messageContent": {"text": history[i][0]}
                })
            schema.append(
                {
                    "chatId": chat_id,
                    "senderId": receiver_id,
                    "receiverId": sender_id,
                    "messageType": "text", 
                    "messageContent": {"text": history[i][1]}
                })
        if schema:
            messages_collection.insert_many(schema)


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

        # Get history data
        schema = list(messages_collection.find({"chatId": self.get_objid(username+'-'+config.appname)}))

        
        chain = Chat_QA_chain_self(model=config.model, temperature=config.temperature, file_path=config.file_path, persist_path=config.db_path, appid=config.appid, api_key=config.api_key, Spark_api_secret=config.Spark_api_secret, Wenxin_secret_key=config.Wenxin_secret_key, embedding=config.embedding, embedding_key=config.embedding_key, template=config.prompt_template, API_DOC=config.API_DOC)

        chain.chat_history = []
        # Use schema.iter to retrieve data
        for i in range(0, len(schema), 2):
            chain.chat_history.append((schema[i].get("messageContent").get("text"), schema[i+1].get("messageContent").get("text")))

        chain.chat_start_index = len(schema)

        chainpoll[username+'-'+config.appname] = chain
        return chain.chat_history
    
    def close_chat(self, username, appname):
        chain = chainpoll.get(username+'-'+appname)
        if not chain:
            raise RuntimeError("Chat 链未开启")
        
        # Save chat history to database
        self.save_history(username, appname, chain.chat_history, chain.chat_start_index)

        chain.clear_history()
        chainpoll.pop(username+'-'+appname)
        return True
    
    def chat_text(self, username, appname, prompt):
        chain = chainpoll.get(username+'-'+appname)
        if not chain:
            raise RuntimeError("Chat 链未开启")
        response = chain.answer(
            question=prompt, userId=self.get_objid_int8(username))
        return response
    
    # Experimental
    def chat_audio(self, username, appname, audio):
        chain = chainpoll.get(username+'-'+appname)
        if not chain:
            raise RuntimeError("Chat 链未开启")
        audio_text = ""
        # Convert audio to text
        # TODO: Add audio to text conversion
        response = chain.answer(question=audio_text,
                                userId=self.get_objid_int8(username))
        return response
    
    def get_history(self, username, appname):
        return chainpoll.get(username+'-'+appname).chat_history
    
    def get_desk_form(self, username, appname):
        # Request from service desk by http request
        service_desk_form_apis = service_desk_collection.find_one({"name": appname}).get("apiEndpoints")
        service_desk_form_api = ""
        for endpoint in service_desk_form_apis:
            print(endpoint)
            if endpoint.get("method") == "GET" and endpoint.get("url").endswith("get_desk_form"):
                service_desk_form_api = endpoint.get("url")
                print(service_desk_form_api)
                break

        if service_desk_form_api == "":
            raise RuntimeError("Service Desk Form API not found")
        try:
            response = requests.get(service_desk_form_api, params={"userId": self.get_objid_int8(username)})
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError("Service Desk API request failed: {}".format(e))        

chatpoll = ChatPool()
