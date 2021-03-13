from gexcel import ExcelBase
from pprint import pprint
from strategy import *
from dynamodbAdapter import dynamodbAdapter

import itertools

class WeeklyUpdate(object):
    def __init__(self, ):
        pass
        self.newclass = None
        self.album = None
        self.todo_table = {'newclass':self.__newClass,
                         'expiredClass':self.__expiredClass,
                         'album':self.__album}
    def weeklyUpdate(self, old):
        
#         ept = {}
#         for to_eb in itertools.product(self.todo, ExcelBase().ongoingTotal().values()):
#             [ ept.update({to_eb[0]+' '+te['{CLASSNAME}']:0}) for te in to_eb[1]]
        '''
            [Dyanamodb]newClass return type: 
                - list
                    - Id: str(uuid4)
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASDATE}: str(NOT isoformat)
                    - {CLASSTIME}: str
                    - {CLASSINTRO}': str
                    - {COVERURL}: str(URL)
            [Dyanamodb]expiredClass return type: 
                - list
                    - Id: str(uuid4)
                    - {CLASSDATE}: str(isoformat)
                    - {ALBUMHASH}: str
        '''
    
        TODO = ['newclass', 'expiredClass']
        todo_res = {}
        on = dynamodbAdapter("dev").putOngoing( 
                                    self.todo_table[TODO[0]]()
                                )
        al = dynamodbAdapter("dev").putAlbum( 
                                    self.todo_table[TODO[1]]()
                                )

    def queryClass(self,):
        return dynamodbAdapter().queryClass()
    
    def __newClass(self, ):
        '''
            return boolean
        '''
        return ExcelBase().newClass()
    def __expiredClass(self, ):
        '''
            檢查課程是否要移到相簿
        '''
        return ExcelBase().expiredClass()
    
    def __album(sellf, ):
        return ExcelBase().albumTotal()
# wu = WeeklyUpdate().weeklyUpdate(None)