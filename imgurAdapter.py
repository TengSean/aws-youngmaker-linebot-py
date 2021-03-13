import json
import requests
from pprint import pprint

from config import Config

import itertools
from itertools import islice, product
import time
import copy

from concurrent.futures import wait, ALL_COMPLETED
from dynamodbAdapter import dynamodbAdapter
from datetime import datetime
from dateutil.relativedelta import relativedelta

class BufferedIter(object):
    def __init__(self, iterator):
        self.iter = iterator
    def nextN(self, n):
        res = []
        try:
            for _ in range(n):
                res.append(next(self.iter))
        except StopIteration as e:
            pass
        return res

class ItemsGenerator(object):
    def __init__(self):
        pass
    def gen(self, default_gen = None):
        for i in default_gen:
            yield i

class Task(object):
    config = Config()
    @classmethod
    def task(cls, **kwargs):
#         albumId = 's9vk1hs'
        url = "https://api.imgur.com/3/album/{}/images".format(kwargs["albumHash"])
        payload = {}
        files = {}
        headers = {
          'Authorization': f'Client-ID {cls.config.imgur_client_id}'
        }

        res = requests.request("GET", url, headers=headers)
        print(res.status_code)
        if res.status_code == 200:
            ret = [ j['link'] for j in json.loads(res.content)['data']]
        else:
            ret = []
        return  ret
# [ j['link'] for j in json.loads(res.content)['data']] 
            
class ImgurAdapter(object):
    def __init__(self, ):
        self.__config = Config()
        self.ig = ItemsGenerator()
        
    def runTask(self, pool_Executor = None, max_Workers = 20, specs=None):
        '''
            Specs list of dict:
                - AlbumHash : str
                - ClassName : str
                - ClassTag : list(str)
                - CreateDate : str(iso)
        '''
        
        futures = dict()
        res = []
        self.bufferediter = BufferedIter(self.ig.gen(default_gen=specs))
        executor = pool_Executor(max_Workers)
        
        while True:
            idle_workers = max_Workers - len(futures)
            items = self.bufferediter.nextN(idle_workers)
            if not items:
                break
            for data in items:
                reg = executor.submit(Task.task, albumHash = data['AlbumHash'])
                futures[reg] = data
            dones, _ = wait(futures, return_when=ALL_COMPLETED)
            
            for f in list(dones):
                futures[f]['AlbumHash'] = f.result()
                res.append(copy.deepcopy(futures[f]))
#                 print(f.result())
                del futures[f]
        return res

