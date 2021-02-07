import configparser

from linebot import (
    LineBotApi, WebhookHandler 
)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(self, file ='./config/config.ini'):
        self.config = configparser.ConfigParser()
        self.check_file(file)
        self.CHANNEL_SECRET = self.config['LINE_BOT']['CHANNEL_SECRET']
        self.CHANNEL_ACCESS_TOKEN = self.config['LINE_BOT']['CHANNEL_ACCESS_TOKEN']
        self.handler = None
        self.line_bot_api = None
        self.imgur_client_id = self.config['IMGUR']['CLIENT_ID']
        self.imgur_client_secret = self.config['IMGUR']['CLIENT_SECRET']
        self.imgur_refresh_token = self.config['IMGUR']['REFRESH_TOKEN']
        self.line_bot_init()

    def check_file(self, file):
        self.config.read(file)
        if not self.config.sections():
            raise configparser.Error('config.ini not exists')


    def line_bot_init(self, ):
        self.handler = WebhookHandler(self.CHANNEL_SECRET)
        self.line_bot_api = LineBotApi(self.CHANNEL_ACCESS_TOKEN)