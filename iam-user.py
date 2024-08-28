import boto3
from datetime import datetime

def lambda_handler(event, context):
    iam = boto3.client('iam')
    
    users = []
    paginator = iam.get_paginator('list_users')
    
    for page in paginator.paginate():
        for user in page['Users']:
            user_info = {
                'UserName': user['UserName'],
                'CreateDate': user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S'),
                'AccessKeys': []
            }
            
            key_paginator = iam.get_paginator('list_access_keys')
            for key_page in key_paginator.paginate(UserName=user['UserName']):
                for key in key_page['AccessKeyMetadata']:
                    key_info = {
                        'AccessKeyId': key['AccessKeyId'],
                        'Status': key['Status'],
                        'CreateDate': key['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
                    }
                    user_info['AccessKeys'].append(key_info)
            
            users.append(user_info)
    
    return {
        'statusCode': 200,
        'body': users
    }