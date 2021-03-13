from flask import jsonify
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
import datetime, time
import uuid, types, logging

from gexcel import ExcelBase
from pprint import pprint


# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

IS_OFFLINE = True
# IS_OFFLINE = os.environ.get('IS_OFFLINE')
# USERS_TABLE = os.environ['USERS_TABLE']
if IS_OFFLINE:
    print('Dynamodb offline mode')
    dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
else:
    print('Dynamodb online mode')
    client = boto3.client('dynamodb')

# https://stackoverflow.com/questions/55286446/getting-http-response-from-boto3-table-batch-writer-object
def _flush(self):
    items_to_send = self._items_buffer[:self._flush_amount]
    self._items_buffer = self._items_buffer[self._flush_amount:]
    self._response = self._client.batch_write_item(
        RequestItems={self._table_name: items_to_send})
    unprocessed_items = self._response['UnprocessedItems']

    if unprocessed_items and unprocessed_items[self._table_name]:
        # Any unprocessed_items are immediately added to the
        # next batch we send.
        self._items_buffer.extend(unprocessed_items[self._table_name])
    else:
        self._items_buffer = []
#     pprint(items_to_send)
#     pprint(self._items_buffer)
#     logger.debug("Batch write sent %s, unprocessed: %s",
#                  len(items_to_send), len(self._items_buffer))

class dynamodbAdapter(object):
    def __init__(self, st="dev"):
        self.__gexcel = ExcelBase()
        self.__stage = st

        
    def putOngoing(self, ongoing):
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
        '''
        timeStamp = datetime.datetime.now().isoformat()
        lastUpdate = timeStamp
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-class-{self.__stage}')
        
#         print(ongoing)
        with table.batch_writer(overwrite_by_pkeys=['ClassName', 'ClassLabel', 'CreateDate']) as batch:
            batch._flush=types.MethodType(_flush, batch)
            for o in ongoing:
                Date = o['{CLASSDATE}'].split('-') if '-' in o['{CLASSDATE}'] else [o['{CLASSDATE}'], o['{CLASSDATE}']]
                Time = o['{CLASSTIME}'].split('-') if '-' in o['{CLASSTIME}'] else [o['{CLASSTIME}'], o['{CLASSTIME}']]
                item = {
                    'Id':o['{ID}'],
                    'ClassName': o['{CLASSNAME}'],
                    'ClassLabel': o['{CLASSTAG}'].split('#')[1],
                    'ClassTag': [  tag for tag in o['{CLASSTAG}'].split('#') if tag ],
                    'ClassIntro': o['{CLASSINTRO}'],
                    'CoverURL': o['{COVERURL}'],
                    
                    'CreateDate': datetime.datetime.strptime(f'{Date[0]} {Time[0]}', "%Y/%m/%d %H:%M").isoformat(),
                    'CloseDate': datetime.datetime.strptime(f'{Date[1]} {Time[1]}', "%Y/%m/%d %H:%M").isoformat(),
                    
                    'TimeStamp':timeStamp,
                    'LastUpdate':lastUpdate
                }
#                 pprint(item)
                batch.put_item(Item=item)
        
        return batch._response

    def putAlbum(self,albums):
#         print("[putAlbum]")
        lastUpdate = datetime.datetime.now().isoformat()
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-class-{self.__stage}')
        print(albums)
        for album in albums:
            print(album['{CLASSNAME}'], album['{CREATEDATE}'])
            key = { 'ClassName': album['{CLASSNAME}'], 'CreateDate':album['{CREATEDATE}'] }
            table.update_item(
                Key = key,
                UpdateExpression="SET AlbumHash = :new_albumHash, LastUpdate = :lastUpdate",
                ExpressionAttributeValues={':new_albumHash':album['{ALBUMHASH}'], ':lastUpdate':lastUpdate},
                ReturnValues = "UPDATED_NEW"
            )
        
    def getAlbum(self ,ClassLabel):
        print("[getAlbum]")
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb', region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-class{self.__stage}')
#         with table.batch_writer(overwrite_by_pkeys=['ClassName', 'ClassLabel', 'CreateDate']) as batch:
#             batch.update_item(
#                 Key={
#                     'Id': '1',
#                     'category': 'class'
#                 },
#                 UpdateExpression="SET #newkey = :newvalue",
#                 ExpressionAttributeNames={'#newkey':'online'},
#                 ExpressionAttributeValues={':newvalue': True},
#                 ReturnValues="UPDATED_NEW"
#             )
        
    def getClass(self,):
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('YoungMaker-basic')
        try:
            res = table.get_item(Key={'Id': '2', 'category': 'class'})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return res['Item']
        
    def queryClass(self, **kwargs):
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-class-{self.__stage}')
        
        if 'year' in kwargs:
            qyear = kwargs['year']
        else:
            qyear = '2001'
        if 'month' in kwargs:
            qmonth = kwargs['month']
        else:
            qmonth = '01'
        if 'classLabel' in kwargs:
            qclassLabel = kwargs['classLabel']
        else :
            qclassLabel = '帶狀課'
        if 'classTag' in kwargs:
            qclassTag = kwrags['classTag']
        else:
            if 'classLabel' in kwargs:
                qclassTag = [kwargs['classLabel']]
            else:
                qclassTag = ['帶狀課']
        if 'projection' in kwargs:
            res = table.query(
                            IndexName = "ClassLabel-CreateDate-index",
                            KeyConditionExpression='ClassLabel = :qclassLabel and CreateDate >= :qDate',
                            ProjectionExpression= ",".join(kwargs['projection']),
                            FilterExpression='attribute_exists(#albumhash)',
                            ExpressionAttributeNames={'#albumhash':'AlbumHash'},
                            ExpressionAttributeValues={
                                ':qclassLabel': qclassLabel,
                                ':qDate': datetime.datetime.strptime(f"{qyear}-{qmonth}-01","%Y-%m-%d").isoformat(),
                            }
                        )
        else:
            res = table.query(
                IndexName = "ClassLabel-CreateDate-index",
                KeyConditionExpression='ClassLabel = :qclassLabel and CreateDate > :qDate',
                FilterExpression='attribute_exists(#albumhash)',
                ExpressionAttributeNames={'#albumhash':'AlbumHash'},
                ExpressionAttributeValues={
                    ':qclassLabel': qclassLabel,
                    ':qDate': datetime.datetime.strptime(f"{qyear}-{qmonth}-01","%Y-%m-%d").isoformat(),
                }
            )
        return res
    
    def updateClass(self,):
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('YoungMaker-basic')
        response = table.update_item(
            Key={
                'Id': '1',
                'category': 'class'
            },
            UpdateExpression="SET #newkey = :newvalue",
            ExpressionAttributeNames={'#newkey':'online'},
            ExpressionAttributeValues={':newvalue': True},
            ReturnValues="UPDATED_NEW"
        )
        
        return response
    
    
    def putUser(self,Id, name):
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-user-{self.__stage}')
        item = {
            'Id':Id,
            'Name':name
        }
        res = table.put_item(Item=item)
        return res
    
    def updateUser(self, Id):
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-user-{self.__stage}')
        res = table.update_item(
            Key={
                'Id': '0',
            },
            UpdateExpression="SET #ri = list_append(#ri, :vals)",
            ExpressionAttributeNames={'#ri':'Ids'},
            ExpressionAttributeValues={':vals': [Id]},
            ReturnValues="UPDATED_NEW"
        )
        return res
    def getUser(self, ):
        if IS_OFFLINE:
            dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'youngmaker-user-{self.__stage}')
        try:
            res = table.get_item(Key={'Id': '0'})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return res['Item']

# if __name__ == '__main__':
#     pprint(dynamodbAdapter().putUser())
#     pprint(dynamodbAdapter().updateUser())
#     pprint(dynamodbAdapter().getUser())
    
#     res = dynamodbAdapter().putAllClass("The Big New Movie", 2015,
#                            "Nothing happens at all.", 0)
#     res = dynamodbAdapter().getClass()
#     res = dynamodbAdapter("dev").queryClass()
#     res = dynamodbAdapter("dev").queryClass(year='2022', projection = ['AlbumHash', 'ClassName', 'ClassTag', 'CreateDate'])

#     pprint(res['Items'])