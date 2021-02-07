from gexcel import ExcelBase
from pprint import pprint
from strategy import *
from dynamodbAdapter import dynamodbAdapter

import itertools

class WeeklyUpdate(object):
    def __init__(self, ):
        pass
        self.todo = ['最新課程', '我要報名']
        
    def weeklyUpdate(self, old):
#         ept = {}
#         for to_eb in itertools.product(self.todo, ExcelBase().ongoingTotal().values()):
#             [ ept.update({to_eb[0]+' '+te['{CLASSNAME}']:0}) for te in to_eb[1]]
#         print(res)
#         pprint(ept)
#             pprint(to_eb)
#             old[]
#             pass
        newclass = self.__newClass()
        if newclass:
#             dynamodb
            pprint(newclass)
        else:
            # Do nothing.
            pass
        
    def __newClass(self, ):
        '''
            return boolean
        '''
        return ExcelBase().newClass()
# wu = WeeklyUpdate().weeklyUpdate(None)
