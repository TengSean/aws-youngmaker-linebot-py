class Bot(object):
    def __init__(self ,msg, lineID):
        self.__msg = msg
        self.__lineID = lineID
        self.template = {}
    def strategy_action(self, ):
        strategy_class = None
        action_func = None
        content = None
        if self.__msg in self.template:
            pass
        return strategy_class, action_func
        