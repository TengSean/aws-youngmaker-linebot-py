from strategy import CarouselFlexStrategy, TextStrategy


from strategy import QA
from strategy import ongoing, signup
from strategy import stripe, camp, weekend
from strategy import stp
from strategy import currentclass

from strategy import follow

from msgHandler import MsgHandler
from valuesHandler import ValuesHandler

from weekUpdate import WeekUpdate


class Bot(object):
    def __init__(self, mtype, lid, msg=None, verb = None):
        
        # begin postback parser.
        if verb:
            self.__verb = verb.split(' ')[0]
            self.__msg = verb.split(' ')[1]
#             self.__verb = data.split('&')[1]
        else:
            self.__verb = None
            self.__msg = msg
        # end postback parser.

        self.__mtype = mtype
        self.__lineID = lid
        
        self.message_flex = {
            'QA': QA,
            '帶狀課 最新課程':stripe, '假日活動 最新課程':weekend, '寒暑假營隊 最新課程':camp,
            'stp': stp
        }
        self.message_short = {
            '最新課程': ongoing,
#             '我要報名':signup,
#             ''
        }
        self.action_short = {
            'follow':follow,
        }
        
        
        self.postback_verb = {
            '您目前點選':None,
            '我要報名':None,
            '詳細資訊':None,
        }
        # 處理event action.
        # eg: follow, join etc..
        self.strategy_map = {
            'message':self.strategyMessage(),
            'postback':self.strategyPostback(),
            'follow':self.strategyAction(),
        }
        self.message_short = self.__set_MessageShort()
    def __set_MessageShort(self,):
        
        return WeekUpdate().weekUpdate(self.message_short)
    
    def strategy(self):
        return self.strategy_map[self.__mtype]
        
    def strategyMessage(self, ):
        strategy_class = None
        message_func = None
        args = None
        if self.__msg in self.message_flex:
            
            if self.__verb in self.postback_verb:
                # Do postback event
#                 message_func = self.postback_verb[]
                if self.__verb == '您目前點選':
                    args = {'{CLASSNAME}':self.__msg}
                    strategy_class = TextStrategy
                    message_func = currentclass
                
            else:
                args = ValuesHandler().valuesHandler(self.__msg)
#                 print(args)
                strategy_class = CarouselFlexStrategy
                message_func = self.message_flex[self.__msg]

                
            
        elif self.__msg in self.message_short:
            # 若有postback 動詞則做
            if self.__verb in self.postback_verb:
                # Do postback event

                pass
            # 否則單純吐出訊息
            else:
                strategy_class = TextStrategy
                message_func = self.message_short[self.__msg]
                
            
        return strategy_class, message_func, args
            
    def strategyPostback(self, ):
        strategy_class = None
        postback_func = None
        args = None
        print(self.__verb)
        if self.__verb in self.postback_verb:
            args = {'{CLASSNAME}':self.__msg}
            strategy_class = TextStrategy
            postback_func = currentclass
        return strategy_class, postback_func, args
    
    # action without msg and data.
    # action only react with mtype.
    def strategyAction(self,):
        strategy_class = None
        action_func = None
        args = None
        if self.__mtype in self.action_short:
            strategy_class = TextStrategy
            action_func = self.action_short[self.__mtype]
            
        return strategy_class, action_func, args
        