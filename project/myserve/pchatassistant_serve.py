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



import env
import os
import sys
import random
import uvicorn
from datetime import datetime, timedelta
from oauth2 import Token, OAuth2PasswordRequestForm, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from oauth2 import get_current_user
from fastapi import FastAPI, Depends, HTTPException, status
from chatService import chatpoll, ChatConfig
# 导入功能模块目录
sys.path.append("../")

app = FastAPI() # 创建 api 对象
API_VER = os.getenv("API_VER", "v1") # 获取 API 版本


@app.post(f"/api/{API_VER}/open_chat")
async def open_chat(conf: ChatConfig, user: str = Depends(get_current_user)):
    # 调用 Chat 链
    if chatpoll.openchat(user, conf):
        return "Chat 链已经开启"
    
@app.post(f"/api/{API_VER}/close_chat")
async def close_chat(appname: str, user: str = Depends(get_current_user)):
    # 关闭 Chat 链
    if chatpoll.close_chat(user, appname):
        return "Chat 链已经关闭"
    
@app.post(f"/api/{API_VER}/clear_history")
async def clear_history(user: str = Depends(get_current_user)):
    # 清空历史记录
    return chatpoll.clear_history(user)

@app.post(f"/api/{API_VER}/chat_text")
async def get_response(prompt: str, appname: str, user: str = Depends(get_current_user)):   
    return {"response": chatpoll.chat_text(user, appname, prompt) }

@app.post(f"/api/{API_VER}/chat_audio")
async def get_response(audio: str, appname: str, user: str = Depends(get_current_user)):
    return {"response": chatpoll.chat_audio(user, appname, audio) }


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




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)