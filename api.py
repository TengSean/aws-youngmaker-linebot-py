from flask import Flask, request, abort, jsonify, render_template, make_response
from config import Config
from weeklyUpdate import WeeklyUpdate
from pprint import pprint

import logging
import time
import datetime
from Bot import Bot
import json

import os

from dynamodbAdapter import dynamodbAdapter
from webAdapter import WebAdapter

import boto3, botocore

from linebot import (
        LineBotApi, WebhookHandler
)

from linebot.exceptions import (
        InvalidSignatureError
)

from linebot.models import (
        MessageEvent, PostbackEvent, FollowEvent,
        TextMessage, TextSendMessage, 
)

app = Flask(__name__)
cf = Config()

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
#     client = boto3.client(
#             'dynamodb',
#             region_name = 'localhost',
#             endpoint_url = 'http://localhost:8000'
#             )
    dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")

else:
#     client = boto3.client('dynamodb')
    dynamodb = boto3.resource('dynamodb')
    
# 以下是dynamodb測試
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

@app.route('/put_test')
def put_test():
#     print ("Hello")
    WeeklyUpdate().weeklyUpdate(None)
    return ("nothing")


@app.route('/get_test')
def get_test():
#     print ("Hello")
#     WeeklyUpdate().weeklyUpdate(None)
    pprint(WeeklyUpdate().queryClass())
    return ("nothing")


@app.route('/')
@app.route('/index')
def index():
    
    Description = [{'cate':'category1', 'name':'category1'}, {'cate':'category2', 'name':'category2'}]
    Item = [
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    {'pile':'a','url':'static/images/1/1.jpg'},
    ]
    
    Item_tmp = WebAdapter().webAdapter(ClassLabel = '帶狀課')
    Item = []
    _ = [ Item.extend(vv) for k,v in Item_tmp.items() for kk, vv in v.items()]
#     pprint(res)

    return render_template("index3.html", Items=Item)



@app.route('/sendmsg')
def sendMsg():
    return render_template('sendmsg.html')
    

# def load_Generator():
db = list()  # The mock database

posts = 500  # num posts to generate

quantity = 20  # num posts to return per request

for x in range(posts):
    db.append(x)

@app.route("/load")
def load():
    """ Route to return the posts """
#     time.sleep(0.2)  # Used to simulate delay
#     Generator()
    if request.args:
        
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(db[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res


# 以下是dynamodb程式碼
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

# @cf.handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    lid = event.source.user_id
    mtype = event.type
    print(msg, lid, mtype)
    bot = Bot(mtype=mtype, msg=msg, lid=lid)
    strategy_class, action_func, values = bot.strategy()
    if strategy_class:
#         print(values)
        task = strategy_class(func = action_func.execute, event = event)
        task.execute(values = values)
        task.name = str(action_func)
        return 0
    cf.line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )

@cf.handler.add(FollowEvent)
def handle_follow(event):
    lid = event.source.user_id
    mtype = event.type
    print(dynamodbAdapter().putUser(lid, cf.line_bot_api.get_profile(lid).display_name))
    print(dynamodbAdapter().updateUser(lid))
#     resp = client.put_item(
#         TableName=USERS_TABLE,
#         Item={
#             'UUID': {'S':lid},
#             'category': {'S': 'user'},
#             'userName': {'S': cf.line_bot_api.get_profile(lid).display_name},
#             'timeStamp': {'S': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}
#         }
#     )
#     print(lid)
    
#     bot = Bot(mtype, lid)
#     strategy_class, action_func, values = bot.strategy()
#     task = strategy_class(func = action_func.execute, event = event)
#     task.execute(lid = lid, name = cf.line_bot_api.get_profile(lid).display_name)
#     task.name = str(action_func)
    
#     cf.line_bot_api.reply_message(
#     event.reply_token,
#     TextSendMessage(text=handler_follow(line_bot_api.get_profile(lid).display_name))
#     )

# @cf.handler.add(PostbackEvent)
def handle_postback(event):
#     msg = event.message.text
    lid = event.source.user_id
    verb = event.postback.data
    mtype = event.type
    bot = Bot(mtype, lid, verb = verb)
    strategy_class, action_func, values = bot.strategy()
    if strategy_class:
        task = strategy_class(func = action_func.execute, event = event)
        task.execute(values = values)
        task.name = str(action_func)
    
#     if event.postback.data == 'hello':
#         pass
#     elif event.postback.data == 'refundConfirm':
#         pass
    
if __name__ == '__main__':
        app.run(debug=True)
