import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    client = boto3.client('secretsmanager')
    
    secrets = []
    paginator = client.get_paginator('list_secrets')
    
    for page in paginator.paginate():
        for secret in page['SecretList']:
            secret_info = {
                'Name': secret['Name'],
                'CreatedDate': secret['CreatedDate'].strftime('%Y-%m-%d %H:%M:%S'),
                'ARN': secret['ARN']
            }
            
            try:
                secret_value = client.get_secret_value(SecretId=secret['ARN'])
                if 'SecretString' in secret_value:
                    secret_info['Value'] = json.loads(secret_value['SecretString'])
                elif 'SecretBinary' in secret_value:
                    secret_info['Value'] = secret_value['SecretBinary']
            except ClientError as e:
                secret_info['Value'] = f"Error retrieving value: {str(e)}"
            
            secrets.append(secret_info)
    
    return {
        'statusCode': 200,
        'body': json.dumps(secrets, default=str)
    }