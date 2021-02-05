from gexcel import ExcelBase
from pprint import pprint


class MsgHandler(object):
    def __init__(self,):
        self.values = {
            
            '{UUID}':None,
            '{USERNAME}':None,
            '{TIMESTAMP}':None,
            
            '{CLASSINTRO}':None,
            '{CLASSDATE}':None,
            '{CLASSTIME}':None,
            '{CLASSDETAIL}':None,
            
            '{URL}':None,
        }
        self.eb = ExcelBase()
    def msgHandler(self, msg):
        if msg == '假日活動 最新課程':
            return self.eb.ongoing_week()
        elif msg == '寒暑假營隊 最新課程':
            return self.eb.ongoing_camp()
        elif msg == '帶狀課 最新課程':
            return self.eb.ongoing_stripe()
#         elif msg == ''
        

# pprint(ValuesHandler().valuesHandler('帶狀課'))