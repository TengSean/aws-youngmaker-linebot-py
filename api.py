from flask import Flask, request, abort, jsonify
import logging

import json

import os

import boto3

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
line_bot_api = LineBotApi('XV1X7KidmK44Bs1oKK8JCshs028vWypnmKpcKV0Xv/GGUplLnrccpEBF3YWHqXGXjiqYb+rCIQU3CoZCEKonzERWWuSx3z+/nnx6dRGMUA1LsXe+7CHxqOGHpM8PbPRKt8Ubn68+5WhjhTpPQjwPSQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0d8a150467c7c3629bd50fe6e49a8605')

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


    
    

@app.route("/users", methods=["POST"])
def insert_user():
    user_id =  request.json.get('userId')

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'UserID': {'S':user_id},
            'birth': {'S':'850823'}
        }
    )
    
    
    return jsonify({
        "userId":user_id,
        "birth":'850823'
        })

@app.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'UUID': {'S':user_id},
            'category': {'S': 'user'}
        }
    )
    

    return jsonify({
        "UUID":resp['Item']['UUID']['S'],
        "category": resp['Item']['category']['S'],
        "userName": resp['Item']['userName']['S']
        })

@app.route("/webhook", methods = ['POST'])
def webhook():



    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

#     event = json.loads(body)
#     print(event)
#     token = event['events'][0]['replyToken']
#     if token == "00000000000000000000000000000000":
#         print("You got the magic")
#     else:
#         line_bot_api.reply_message(token, TextSendMessage(
#                 text = event['events'][0]['message']['text']
#                 )
#         )
    return 'OK'

def handler_follow():
    text = '''嗨！{Vicky(高鈺婷)}
歡迎來到YoungMaker創夢積構！
從這裡可以看到課程簡介、最新的課程資訊、
也可以查看歷史課程的相片唷!
我們固定每週一都會更新內容，
趕快點選下方選單，來看看有什麼好玩的課吧！'''
    return text
#   with open('src/reply_template/welcome.txt', 'r') as f:
#     wel_json = eval(f.read())
#   return wel_json

@handler.add(FollowEvent)
def handle_follow(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=handler_follow())
  )
      




# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = event.message.text
    

#     CONFIG.LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(message))

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'UUID': {'S':user_id},
            'category': {'S': 'user'},
            'userName': {'S': line_bot_api.get_profile(user_id).display_name}
        }
    )
    print(user_id)


if __name__ == '__main__':
        app.run(debug=True)
