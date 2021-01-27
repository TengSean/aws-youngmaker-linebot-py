
import abc
import types
from flask import request

from linebot.models import *

from config import Config

class BaseStrategy():

    def __init__(self, func = None, event = None, *args, **kwargs):
        self.name = func.__name__ if func else "default"
        self.__CONFIG = Config()
        self.event = event
        if func:
            self.__execute = types.MethodType(func, self)
        # print('{} class, task {}'.format(self.__class__.__name__, self.name))
    
    def __execute(self, Content=None, *args, **kwargs):
        pass

    def execute(self, Content=None, *args, **kwargs):
        # obj = self.__execute(Content)
        obj = self.__execute(*args, **kwargs)

        # self.reply_message(TextSendMessage(text))   
        self.reply_message(obj)

    def reply_message(self, obj):
        self.__CONFIG.line_bot_api.reply_message(self.event.reply_token, obj)
        
        
class TemplateStrategy(BaseStrategy, metaclass = abc.ABCMeta):
    def __init__(self, func = None, event = None, CarouselColumns = None, ):
        super().__init__(func = func,
                        event = event,
                        CarouselColumns = CarouselColumns)

    @abc.abstractmethod
    def Update_Columns(self, ):
        return NotImplemented

    @abc.abstractmethod
    def get_columns(self, ):
        return NotImplemented
    

class MessageStrategy(BaseStrategy):
    def __init__(self, func = None, event = None):
        super().__init__(func = func,
                        event = event)

    
class FlexStrategy(TemplateStrategy):
    def __init__(self, func = None, event = None, CarouselColumns = None):
        super().__init__(func = func,
                        event = event,
                        CarouselColumns = CarouselColumns)

    def Update_Columns(self, ):
        print('Test update')

    def get_columns(self, ):
        print(self.carouselColumns[0])
        
        
        
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


class ongoing(object):

    def execute(cls, *args, **kwargs):
        return TextSendMessage(text='請選擇課別',
                               quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="假日活動", text="假日活動")),
                                    QuickReplyButton(action=MessageAction(label="帶狀課", text="帶狀課")),
                                    QuickReplyButton(action=MessageAction(label="寒暑假營隊", text="寒暑假營隊"))
                               ]))
class signup(object):
    def execute(cls, *args, **kwargs):
        return TextSendMessage(text='''嗨！請加Vicky老師好友，
並回傳以下報名資訊就可以囉！

姓名：
年級：
學校：
報名課程：

若有其他課程相關的問題，也可以直接詢問哦😊''')
        
    
    
class weekend(object):
#     __json = jsonParser()
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/weekend.txt', 'r') as f:
            flex_json = eval(f.read())
        return FlexSendMessage(
                alt_text = f'flex notify',
                contents = flex_json
            )

class stripe(object):
#     __json = jsonParser()
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/stripe.txt', 'r') as f:
            flex_json = eval(f.read())
        return FlexSendMessage(
                alt_text = f'flex notify',
                contents = flex_json
            )

class camp(object):
#     __json = jsonParser()
    def execute(cls, *args, **kwargs):
        with open('src/reply_template/camp.txt', 'r') as f:
            flex_json = eval(f.read())
        return FlexSendMessage(
                alt_text = f'flex notify',
                contents = flex_json
            )