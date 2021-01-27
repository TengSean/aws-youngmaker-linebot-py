from strategy import FlexStrategy, MessageStrategy


from strategy import QA
from strategy import ongoing, signup
from strategy import stripe, camp, weekend


class Bot(object):
    def __init__(self ,msg, lid, data = None):
        if data:
            self.__msg = data.split('&')[0]
            self.__data = data.split('&')[1]
        else:
            self.__msg = msg
            self.__data = None
        self.__lineID = lid
        self.flex = {
            'QA': QA,
            '帶狀課':stripe,
            '假日活動':weekend,
            '寒暑假營隊':camp,
        }
        self.shortReply = {
            '近期課程': ongoing,
            '我要報名':signup

        }
        
    def strategy_action(self, ):
        strategy_class = None
        action_func = None
        args = None
        if self.__msg in self.flex:
            strategy_class = FlexStrategy
            action_func = self.flex[self.__msg]
            if self.__data:
                # Do postback event
                pass
            
            
        elif self.__msg in self.shortReply:
            strategy_class = MessageStrategy
            action_func = self.shortReply[self.__msg]
            if self.__data:
                # Do postback event
                pass
            
            
            

        return strategy_class, action_func, args
        