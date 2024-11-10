import boto3
from .entities import Repository
from flask import current_app


class DynamoDBRepository(Repository):
    def __init__(self, table_name, endpoint_url=None):
        self.table_name = table_name
        self.endpoint_url = endpoint_url
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endpoint_url)
        self.table = self.dynamodb.Table(self.table_name)
  
    def store(self, id, data):
        response = self.table.put_item(Item={'game_id': id, 'data': data})
        return response

    def retrieve(self, id):
        current_app.logger.debug(f"Buscando item {id}")
        response = self.table.get_item(Key={'game_id': id})
        if 'Item' not in response:
            raise KeyError(f"Item {id} not found")
        return response.get('Item').get("data")
