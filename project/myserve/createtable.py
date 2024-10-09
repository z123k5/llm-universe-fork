from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from datetime import datetime

# 连接到 MongoDB
def connect_to_database():
    try:
        client = MongoClient('mongodb://root:123456jqk*@localhost:27017/assistant_proj', 
                             serverSelectionTimeoutMS=30000, 
                             socketTimeoutMS=45000)
        client.admin.command('ping')
        print('成功连接到 MongoDB')
        return client
    except ConnectionFailure as e:
        print('连接到 MongoDB 时出错:', e)
        return None

client = connect_to_database()
db = client.assistant_proj if client else None

# 用户 Schema
user_schema = {
    "username": {"type": "string", "unique": True, "required": True},
    "displayName": {"type": "string", "required": True},
    "email": {"type": "string", "unique": True, "required": True},
    "passwordHash": {"type": "string", "required": True},
    "profileImageUrl": {"type": "string"},
    "status": {"type": "string", "enum": ["online", "offline", "busy"], "default": "offline"},
    "lastSeen": {"type": "date", "default": datetime.now},
    "friends": [{"type": "ObjectId", "ref": "User"}],
    "blockedUsers": [{"type": "ObjectId", "ref": "User"}],
    "settings": {
        "notifications": {"type": "boolean", "default": True},
        "privacy": {"type": "string", "enum": ["public", "private"], "default": "public"}
    }
}

# 聊天消息 Schema
message_schema = {
    "chatId": {"type": "ObjectId", "required": True, "index": True},
    "senderId": {"type": "ObjectId", "ref": "User", "required": True, "index": True},
    "receiverId": {"type": "ObjectId", "ref": "User", "required": True},
    "messageType": {"type": "string", "enum": ["text", "image", "audio", "video", "link"], "required": True},
    "messageContent": {
        "text": {"type": "string"},
        "fileUrl": {"type": "string"},
        "thumbnailUrl": {"type": "string"},
        "audioDuration": {"type": "number"}
    },
    "sentAt": {"type": "date", "default": datetime.now},
    "receivedAt": {"type": "date"},
    "status": {"type": "string", "enum": ["sent", "delivered", "read"], "default": "sent"}
}

# 机器人助理 Schema
assistant_schema = {
    "id": {"type": "string", "required": True, "unique": True},
    "name": {"type": "string", "required": True},
    "description": {"type": "string", "required": True},
    "corpus": {
        "path": {"type": "string", "required": True},
        "lastUpdated": {"type": "date", "default": datetime.now}
    },
    "behaviorLibrary": {
        "path": {"type": "string", "required": True},
        "lastUpdated": {"type": "date", "default": datetime.now}
    },
    "promptEngineeringLibrary": {
        "path": {"type": "string", "required": True},
        "lastUpdated": {"type": "date", "default": datetime.now}
    }
}

# 服务台 Schema
service_desk_schema = {
    "id": {"type": "string", "required": True, "unique": True},
    "name": {"type": "string", "required": True},
    "description": {"type": "string", "required": True},
    "apiDocuments": {
        "path": {"type": "string", "required": True},
        "lastUpdated": {"type": "date", "default": datetime.now}
    },
    "apiEndpoints": [
        {
            "url": {"type": "string", "required": True},
            "method": {"type": "string", "required": True},
            "parameters": {"type": "object", "required": True}
        }
    ]
}

# 创建集合并插入数据
if True:
    user_collection = db.users
    message_collection = db.messages
    assistant_collection = db.assistants
    service_desk_collection = db.service_desks

    # 插入用户数据
    user = {
        "username": "z123k5",
        "displayName": "zk",
        "email": "123456789@qq.com",
        "passwordHash": "1234567"
    }
    user_collection.insert_one(user)

    # 插入聊天消息数据
    message = {
        "chatId": ObjectId(),
        "senderId": ObjectId(),
        "receiverId": ObjectId(),
        "messageType": "text",
        "messageContent": {
            "text": "Hello, World!"
        }
    }
    message_collection.insert_one(message)

    # 插入机器人助理数据
    assistant = {
        "id": str(ObjectId()),
        "name": "餐馆服务员助理",
        "description": "一个虚拟的餐馆服务员",
        "corpus": {
            "path": "/../../../data_base/data_base/vector_db/chroma"
        },
        "behaviorLibrary": {
            "path": "/../../../data_base/data_base/knowledge_db"
        },
        "promptEngineeringLibrary": {
            "path": "/restaurant_assist/prompt_template.txt"
        }
    }
    assistant_collection.insert_one(assistant)

    # 插入服务台数据
    service_desk = {
        "id": "4",
        "name": "餐馆服务员助理",
        "description": "一个虚拟的餐馆服务员",
        "apiDocuments": {
            "path": "/restaurant_assist/api_doc.txt",
        },
        "apiEndpoints": [
            {
                "url": "http://localhost:3000/api/v1/menu",
                "method": "GET",
                "parameters": {
                    "restaurantId": 5
                }
            }
        ]
    }
    service_desk_collection.insert_one(service_desk)