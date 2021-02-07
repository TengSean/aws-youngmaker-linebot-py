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

USERS_TABLE = 'YoungMaker-basic'
IS_OFFLINE = True
# USERS_TABLE = os.environ['USERS_TABLE']
# IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
#     client = boto3.client(
#             'dynamodb',
#             region_name = 'localhost',
#             endpoint_url = 'http://localhost:8000'
#             )
    dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
else:
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
    def __init__(self,):
        self.__gexcel = ExcelBase()
        

        
    def initClass(self, classes):
        createDate = datetime.datetime.now().isoformat()
        lastUpdate = createDate
        dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('YoungMaker-basic')
        with table.batch_writer() as batch:
            batch._flush=types.MethodType(_flush, batch)
            for k, v in classes.items:
                for vv in v:
#                             camp = [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{URL}':url[0] } for name, intro, url in zip(camp_name, camp_intro, camp_url)]

                    batch.put_item(
                        {
                        'Id': vv['{ID}'],
                        'category': 'class',
                        'className': vv['{CLASSNAME}'],
#                         'classDate': vv['{CLASSDATE}'],
                        'classIntro': vv['{CLASSINTRO}'],
                        'coverURL': vv['COVERURL'],
                        }
                    )
        
        return batch._response


    def getClass(self,):
        dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('YoungMaker-basic')
        try:
            res = table.get_item(Key={'Id': '2', 'category': 'class'})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return res['Item']
        
    def queryClass(self, ):
        dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('YoungMaker-basic')

        res = table.query(
                        KeyConditionExpression='Id = :artist',
                        ExpressionAttributeValues={
                            ':artist': {'S': '1'}
#                             ':artist': {'S': 'ed8a47dd-17c6-4a06-8895-59d77e30d26f'}
                        }
                    )
        return res
    
    def updateClass(self,):
        dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
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
if __name__ == '__main__':
    res = dynamodbAdapter().putAllClass("The Big New Movie", 2015,
                           "Nothing happens at all.", 0)
#     res = dynamodbAdapter().getClass()
#     res = dynamodbAdapter().queryClass()
#     res = dynamodbAdapter().updateClass()
    print("Put movie succeeded:")
    pprint(res)