from gexcel import ExcelBase
from pprint import pprint
from strategy import *


import itertools

class WeekUpdate(object):
    def __init__(self, ):
        pass
        self.todo = ['最新課程', '我要報名']
        
    def weekUpdate(self, old):
        ept = {}
        for to_eb in itertools.product(self.todo, ExcelBase().ongoing_total().values()):
            res = [ ept.update({to_eb[0]+' '+te['{CLASSNAME}']:0}) for te in to_eb[1]]
            pprint(ept)
#             pprint(to_eb)
#             old[]
#             pass


# wu = WeekUpdate().weekUpdate(None)
