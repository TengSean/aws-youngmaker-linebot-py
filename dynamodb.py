from flask import jsonify
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
import datetime, time
import uuid

from gexcel import ExcelBase
from pprint import pprint

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


class dynamodbAdapter(object):
    def __init__(self,):
        self.__gexcel = ExcelBase()
        
    def putAllClass(self, title, year, plot, rating, dynamodb=None):
        Id = uuid.uuid4()
        createDate = datetime.datetime.now().isoformat()
        lastUpdate = createDate
#         dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('YoungMaker-basic')
#         with table.batch_w
        res = table.put_item(
                            Item={
                                'Id': '1',
                                'category': 'class',
                            }
        )
#         print('http://'+str(classUID))
        
        return res


    def getClass(self,):
        dynamodb = boto3.resource('dynamodb',region_name = 'localhost', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('YoungMaker-basic')
        try:
            res = table.get_item(Key={'Id': '1', 'category': 'class'})
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
#     res = dynamodbAdapter().putAllClass("The Big New Movie", 2015,
#                            "Nothing happens at all.", 0)
#     res = dynamodbAdapter().getClass()
#     res = dynamodbAdapter().queryClass()
#     res = dynamodbAdapter().updateClass()
    print("Put movie succeeded:")
    pprint(res)