from dynamodbAdapter import dynamodbAdapter
from imgurAdapter import ImgurAdapter


from concurrent.futures import ProcessPoolExecutor
from pprint import pprint
from itertools import groupby
from operator import itemgetter
from collections import defaultdict


class WebAdapter(object):
    def __init__(self, ):
        pass
    
    
    def webAdapter(self,ClassLabel, Year=None, Month=None):
        '''
            [dynamodbAdapter]queryClass return type: 
                - dict
                    - AlbumHash: str
                    - ClassName: str
                    - ClassTag: str
                    - CreateDate: str(isoformat)
            [ImgurAdapter]runTask return type: 
                - list
                    - AlbumHash: list(url)
                    - ClassName: str
                    - ClassTag: str
                    - CreateDate: str(isoformat)
        '''
        
        specs = dynamodbAdapter("dev").queryClass(classLabel = ClassLabel,
                                                  projection = ['AlbumHash', 'ClassName', 'ClassTag', 'CreateDate'])
#         pprint(specs)
        if specs['Items']:
            res = ImgurAdapter().runTask(pool_Executor = ProcessPoolExecutor,
                                         max_Workers = 30,
                                         specs = specs['Items'])
#             pprint(res)
            return self.groupByDate(res)
        else:
            print('queryClass album return empty!')
            return -1
        
    def groupByDate(self, res):
        tmpl = []
        grp_after = {}
        grp_before = [ [r['CreateDate'].split('-')[0], r['CreateDate'].split('-')[1], r] for r in res]
#         pprint(grp_before)
        for year, ygrp in groupby(grp_before, key=itemgetter(0)):
            for month , mgrp in groupby(ygrp, key=itemgetter(1)):
                if year not in grp_after:
                    grp_after[year] = {}
                if month not in grp_after[year]:
                    grp_after[year][month] = [grp[-1] for grp in list(mgrp) ]
                else:
                    grp_after[year][month].extend([grp[-1] for grp in list(mgrp) ])
#                 print(month)
#                 pprint(list(mgrp))
        pprint(grp_after)
        return grp_after
WebAdapter().webAdapter(ClassLabel = '帶狀課')
# pprint(WebAdapter().webAdapter(ClassLabel = '帶狀課')['2020']['09'])
