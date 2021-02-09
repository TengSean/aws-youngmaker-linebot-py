import json
import requests
from pprint import pprint

from config import Config

class ImgurAdapter(object):
    def __init__(self, ):
        self.__config = Config()
        
    def getAlbum(self, albumId):
#         albumId = 's9vk1hs'
        url = f"https://api.imgur.com/3/album/{albumId}/images"

        payload = {}
        files = {}
        headers = {
          'Authorization': f'Client-ID {self.__config.imgur_client_id}'
        }

        res = requests.request("GET", url, headers=headers)
        
        return [ j['link'] for j in json.loads(res.content)['data']]
        
        
# ia = ImgurAdapter().imgurAdapter()