#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pchatassistant_serve.py
@Time    :   2024/10/01
@Author  :   Kang
@Version :   1.0
@Contact :   1994918916@qq.com
@License :   (C)Copyright 2024
@Desc    :   启动 ChatAssistant 服务
'''



from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import env
import os
import sys
import random
import uvicorn
from datetime import datetime, timedelta
from oauth2 import Token, OAuth2PasswordRequestForm, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from oauth2 import get_current_user
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from chatService import chatpoll, ChatConfig
# 导入功能模块目录
sys.path.append("../")

app = FastAPI() # 创建 api 对象
API_VER = os.getenv("API_VER", "v1") # 获取 API 版本

# CORS 设定只允许localhost访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(f"/api/{API_VER}/open_chat")
async def open_chat(conf: ChatConfig, user: str = Depends(get_current_user)):
    # 调用 Chat 链
    hist = chatpoll.openchat(user, conf);
    if isinstance(hist, list) or hist == True:
        return hist
    else:
        return "找不到 app"
    
@app.post(f"/api/{API_VER}/close_chat")
async def close_chat(appname: str, user: str = Depends(get_current_user)):
    # 关闭 Chat 链
    if chatpoll.close_chat(user, appname):
        return "Chat 链已经关闭"
    else:
        return "未找到 Chat链"
    
@app.post(f"/api/{API_VER}/clear_history")
async def clear_history(appname: str, user: str = Depends(get_current_user)):
    # 清空历史记录
    return chatpoll.clear_history(user, appname)

@app.post(f"/api/{API_VER}/chat_text")
async def get_response(prompt: str, appname: str, user: str = Depends(get_current_user)):
    try:
        rensponce = chatpoll.chat_text(user, appname, prompt)
        return {"response": rensponce }
    except Exception as e:
        return  JSONResponse(content={"response": str(e) }, status_code=500, media_type="application/json")

@app.post(f"/api/{API_VER}/chat_audio")
async def get_response(audio: str, appname: str, user: str = Depends(get_current_user)):
    try:
        rensponce = chatpoll.chat_audio(user, appname, audio)
        return {"response": rensponce}
    except Exception as e:
        return JSONResponse(content={"response": str(e)}, status_code=500, media_type="application/json")

@app.post(f"/api/{API_VER}/get_desk_form")
async def get_response(appname: str, user: str = Depends(get_current_user)):
    try:
        response = chatpoll.get_desk_form(user, appname)
        return {"response": response }
    except Exception as e:
        return JSONResponse(content={"response": str(e)}, status_code=500, media_type="application/json")


@app.post(f"/api/{API_VER}/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Route to login and get access token

    Args:
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@app.get(f"/api/{API_VER}/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    """Route to check current user

    Args:
        current_user (_type_, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    return {"status": "active"}


@app.post(f"/api/{API_VER}/users/log_out")
async def log_out(current_user = Depends(get_current_user)):
    """Route to log out

    Args:
        current_user (_type_, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    return {"status": "logged out"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)