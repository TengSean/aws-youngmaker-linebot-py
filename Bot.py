from strategy import FlexStrategy, TextStrategy


from strategy import QA
from strategy import ongoing, signup
from strategy import stripe, camp, weekend
from strategy import follow

class Bot(object):
    def __init__(self, mtype, lid,msg=None, data = None):
        if data:
            self.__msg = data.split('&')[0]
            self.__data = data.split('&')[1]
        else:
            self.__msg = msg
            self.__data = None
        self.__mtype = mtype
        self.__lineID = lid
        
        self.message_flex = {
            'QA': QA,
            '帶狀課':stripe, '假日活動':weekend, '寒暑假營隊':camp,
        }
        
        self.message_short = {
            '近期課程': ongoing,
            '我要報名':signup
        }
        self.action_short = {
            'follow':follow,
        }
        # 處理event action.
        # eg: follow, join etc..
        self.strategy_map = {
            'message':self.strategy_message(),
            'postback':self.strategy_message(),
            'follow':self.strategy_action(),
        }

    def strategy(self):
        return self.strategy_map[self.__mtype]
        
    def strategy_message(self, ):
        strategy_class = None
        action_func = None
        args = None
        if self.__msg in self.message_flex:
            strategy_class = FlexStrategy
            action_func = self.message_flex[self.__msg]
            if self.__data:
                # Do postback event
                pass
            
            
        elif self.__msg in self.message_short:
            strategy_class = TextStrategy
            action_func = self.message_short[self.__msg]
            if self.__data:
                # Do postback event
                pass
        return strategy_class, action_func, args
            
            
    
    # action without msg and data.
    # action only react with mtype.
    def strategy_action(self,):
        strategy_class = None
        action_func = None
        args = None
        if self.__mtype in self.action_short:
            strategy_class = TextStrategy
            action_func = self.action_short[self.__mtype]
            
        return strategy_class, action_func, args
        