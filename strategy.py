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
        self.__CONFIG.LINE_BOT_API.reply_message(self.event.reply_token, obj)