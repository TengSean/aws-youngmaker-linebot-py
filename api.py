from flask import Flask, request, abort, jsonify
from config import Config

import logging
import time
import datetime
from Bot import Bot
import json

import os

import boto3, botocore

from linebot import (
        LineBotApi, WebhookHandler
)

from linebot.exceptions import (
        InvalidSignatureError
)

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage, FollowEvent
)

app = Flask(__name__)
cf = Config()
# line_bot_api = LineBotApi('XV1X7KidmK44Bs1oKK8JCshs028vWypnmKpcKV0Xv/GGUplLnrccpEBF3YWHqXGXjiqYb+rCIQU3CoZCEKonzERWWuSx3z+/nnx6dRGMUA1LsXe+7CHxqOGHpM8PbPRKt8Ubn68+5WhjhTpPQjwPSQdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('0d8a150467c7c3629bd50fe6e49a8605')

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
            'dynamodb',
            region_name = 'localhost',
            endpoint_url = 'http://localhost:8000'
            )
else:
    client = boto3.client('dynamodb')
# dynamodb = boto3.resource('dynamodb')

    
    

@app.route("/users", methods=["POST"])
def insert_user():
    user_id =  request.json.get('userId')
    curtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'UUID': {'S':user_id},
            'category': {'S': 'user'},
            'userName': {'S':'testing'},
            'timeStamp': {'S': curtime}
        }
    )
    
    
    return jsonify({
        "UUID":user_id,
        'category':  'user',
        'userName': 'testing',
        'timeStamp': curtime
        })

@app.route("/users/<string:user_id>")
def get_user(user_id):
#     try:
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'UUID': {'S':user_id},

            'category': {'S': 'user'}
        }
    )
#     except client.exceptions.ResourceNotFoundException as e:
#         print("can't find data.")

    return jsonify({
        "UUID":resp['Item']['UUID']['S'],
        "category": resp['Item']['category']['S'],
        "userName": resp['Item']['userName']['S'],
        "timeStamp": resp['Item']['timeStamp']['S']
        })

@app.route("/webhook", methods = ['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        cf.handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def handler_follow(name):
    text = f'''嗨！{name}
歡迎來到YoungMaker創夢積構！
從這裡可以看到課程簡介、最新的課程資訊、
也可以查看歷史課程的相片唷!
我們固定每週一都會更新內容，
趕快點選下方選單，來看看有什麼好玩的課吧！'''
    return text
#   with open('src/reply_template/welcome.txt', 'r') as f:
#     wel_json = eval(f.read())
#   return wel_json

@cf.handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    lineID = event.source.user_id
    bot = Bot(msg, lineID)
    strategy_class, action_func = bot.strategy_action()
    if strategy_class:
        pass
    cf.line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=msg)
    )

@cf.handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'UUID': {'S':user_id},
            'category': {'S': 'user'},
            'userName': {'S': cf.line_bot_api.get_profile(user_id).display_name},
            'timeStamp': {'S': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}
        }
    )
    print(user_id)
    cf.line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=handler_follow(line_bot_api.get_profile(user_id).display_name))
    )
    
if __name__ == '__main__':
        app.run(debug=True)
