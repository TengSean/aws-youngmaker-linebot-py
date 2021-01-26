from strategy import FlexStrategy, MessageStrategy


from strategy import QA
from strategy import ongoing

class Bot(object):
    def __init__(self ,msg, lineID):
        self.__msg = msg
        self.__lineID = lineID
        self.flex = {
            'QA': QA
            
        }
        self.shortReply = {
            '近期課程': ongoing         
        }
        
    def strategy_action(self, ):
        strategy_class = None
        action_func = None
        content = None
        if self.__msg in self.flex:
            strategy_class = FlexStrategy
            action_func = self.flex[self.__msg]
        elif self.__msg in self.shortReply:
            strategy_class = MessageStrategy
            action_func = self.shortReply[self.__msg]

        return strategy_class, action_func
        