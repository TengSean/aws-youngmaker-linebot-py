import json
import requests
from pprint import pprint

from config import Config

import itertools
from itertools import islice, product
import time

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import wait, ALL_COMPLETED

WAIT_SLEEP = 0.3

class BufferedIter(object):
    def __init__(self, iterator):
        self.iter = iterator
    def nextN(self, n):
        try:
            return [ next(self.iter) for _ in range(n) ]
        except StopIteration as e:
            print(e)
            pass
#             return [ next(self.iter for _ in range())]
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
        url = "https://api.imgur.com/3/album/{}/images".format(kwargs["albumId"])

        payload = {}
        files = {}
        headers = {
          'Authorization': f'Client-ID {cls.config.imgur_client_id}'
        }

        res = requests.request("GET", url, headers=headers)
        
        return  [ j['link'] for j in json.loads(res.content)['data']] 
#         print ( [ j['link'] for j in json.loads(res.content)['data']] )
            
class ImgurAdapter(object):
    def __init__(self, ):
        self.__config = Config()
        self.ig = ItemsGenerator()

    @classmethod
    def task(cls, **kwargs):
#         albumId = 's9vk1hs'
        url = "https://api.imgur.com/3/album/{}/images".format(kwargs["albumId"])

        payload = {}
        files = {}
        headers = {
          'Authorization': f'Client-ID {cls.__config.imgur_client_id}'
        }

        res = requests.request("GET", url, headers=headers)
        
        print( [ j['link'] for j in json.loads(res.content)['data']] )
#         return [ j['link'] for j in json.loads(res.content)['data']]
        
    def runTask(self, pool_Executor = None, max_Workers = 20, specs=['test']):
        futures = dict()
        self.bufferediter = BufferedIter(self.ig.gen(default_gen=specs))
        executor = pool_Executor(max_Workers)
        while True:
            idle_workers = max_Workers - len(futures)
#             print(idle_workers)
#             try:
            items = self.bufferediter.nextN(idle_workers)
#             except StopIteration:
#                 break
            print(items)

            for data in items:
#                 print(data)
                futures[executor.submit(Task.task, albumId = data)] = data
                dones, _ = wait(futures, return_when=ALL_COMPLETED)

            for f in list(dones):
                print(f.result())
                del futures[f]
                    
                    
specs = ['s9vk1hs','s9vk1hs','s9vk1hs','s9vk1hs','s9vk1hs','s9vk1hs','s9vk1hs','s9vk1hs']
st = time.time()

ia = ImgurAdapter().runTask(pool_Executor = ProcessPoolExecutor, max_Workers=30, specs = specs)

ed = time.time()
print(ed-st)