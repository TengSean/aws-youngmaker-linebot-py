import abc
import types
import copy
from flask import request

from linebot.models import *

from config import Config

from gexcel import ExcelBase

from jsonHandler import JsonHandler
from msgHandler import MsgHandler


class BaseStrategy():

    def __init__(self, func = None, event = None, *args, **kwargs):
        self.name = func.__name__ if func else "default"
        self.__CONFIG = Config()
        self.event = event
        if func:
            self.__execute = types.MethodType(func, self)
        # print('{} class, task {}'.format(self.__class__.__name__, self.name))
    
    def __execute(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        # obj = self.__execute(Content)
        obj = self.__execute(*args, **kwargs)

        # self.reply_message(TextSendMessage(text))   
        self.reply_message(obj)

    def reply_message(self, obj):
        self.__CONFIG.line_bot_api.reply_message(self.event.reply_token, obj)
        
        
class CarouselStrategy(BaseStrategy, metaclass = abc.ABCMeta):
    def __init__(self, func = None, event = None, *args, **kwargs):
        super().__init__(func = func,
                        event = event,
                        *args,
                        **kwargs)

    @abc.abstractmethod
    def Update_Columns(self, ):
        return NotImplemented

    @abc.abstractmethod
    def get_columns(self, ):
        return NotImplemented
    

class TextStrategy(BaseStrategy):
    def __init__(self, func = None, event = None):
        super().__init__(func = func,
                        event = event)

    
class CarouselFlexStrategy(CarouselStrategy):
    def __init__(self, func = None, event = None, *args, **kwargs):
        super().__init__(func = func,
                        event = event,
                        *args,
                        **kwargs)

    def Update_Columns(self, msg, values):
        return [  JsonHandler().jsonReplace( copy.deepcopy(msg), value) for value in values]
    def get_columns(self, ):
        print('aa')
        
class follow():
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/welcome.txt', 'r') as f:
            msg = f.read().format(kwargs['name'])
        return TextSendMessage(text=msg)
        
class QA():
    __CAROUSEL_TEMPLATE = CarouselTemplate(
        columns=[
        ]
    )
    __FLEX = FlexSendMessage

    CAROUSEL_COLUMNS = list()
    @classmethod
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/QA.txt', 'r') as f:
            flex_json = eval(f.read())
#         gs = Gshandler()
#         loyalty = gs.get_loyalty(kwargs['lid'])
#         flex_json['body']['contents'][1]['contents'][0]['contents'][1]['text'] = str(loyalty)
        return FlexSendMessage(
                    alt_text = f'flex notify',
                    contents = flex_json
                )


# Fix template
class ongoing():

    def execute(self, *args, **kwargs):
        return TextSendMessage(
            text='請選擇課別',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="假日活動", text="假日活動 最新課程")),
                QuickReplyButton(action=MessageAction(label="帶狀課", text="帶狀課 最新課程")),
                QuickReplyButton(action=MessageAction(label="寒暑假營隊", text="寒暑假營隊 最新課程"))
            ])
        )
    
# 過渡用
class currentclass():
    def execute(self, *args, **kwargs):
        return TextSendMessage(
            text='您目前點選 {}'.format(kwargs['values']["{CLASSNAME}"]),
            quick_reply=QuickReply(items=[
#                 QuickReplyButton(action=MessageAction(label="詳細資訊", text='課程資訊 {}'.format(kwargs['values']["{CLASSNAME}"]))),
                QuickReplyButton(action=PostbackAction(label='詳細資訊', data='課程資訊 {}'.format(kwargs['values']["{CLASSNAME}"]), text="查看{}詳細資訊".format(kwargs['values']['{CLASSNAME}']))),
                QuickReplyButton(action=MessageAction(label="我要報名", text='我要報名 {}'.format(kwargs['values']["{CLASSNAME}"]))),
                QuickReplyButton(action=MessageAction(label="揪團報名", text='我要報名 {}'.format(kwargs['values']["{CLASSNAME}"]))),
            ])
        )

class signup(object):
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/signup_msg.txt', 'r') as f:
            msg = f.read()
        return TextSendMessage(text=msg)
        
    
    
    
# Dyanmic template
class weekend(object):
#     __json = jsonParser()
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/weekend.txt', 'r') as f:
            flex_json = eval(f.read())
        return FlexSendMessage(
                alt_text = f'假日活動最新課程',
                contents = flex_json
            )

# Dyanmic template
class stripe(object):
#     __json = jsonParser()
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/stripe.txt', 'r') as f:
            flex_json = eval(f.read())
        return FlexSendMessage(
                alt_text = f'帶狀課最新課程',
                contents = flex_json
            )

# Dyanmic template
# Set carousel list
class camp():
    def execute(self, *args, **kwargs):
#         print(kwargs['values'])
        with open('src/reply_template/camp_box.txt', 'r') as boxf, open('src/reply_template/camp_element.txt') as elef:
#             flex_json = eval(boxf.read())
            box = eval(boxf.read())
            print(box)

            box['contents'] = self.Update_Columns(
                                        eval(elef.read()),
                                        kwargs['values']       
                                               )
            flex_json = box
#             print(flex_json)
#             flex_json = self.Update_Columns(eval(f.read()), kwargs['args'])
#         print(ExcelBase().ongoing())
        return FlexSendMessage(
                alt_text = f'寒暑假營隊最新課程',
                contents = flex_json,
            )
    
    
    
class stp(object):
#     __json = jsonParser()
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/stp.txt', 'r') as f:
            flex_json = eval(f.read())
        return FlexSendMessage(
                alt_text = f'flex notify',
                contents = flex_json
            )