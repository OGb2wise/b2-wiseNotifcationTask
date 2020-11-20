
import helper
import os
import boto3
from botocore.exceptions import ClientError
import format_helper
import types
from datetime import datetime

client = boto3.client('dynamodb')
Notification_Table = os.environ['Notification_Table']
ErrorMessage=""

def write_data(input):
     global ErrorMessage
     return_value = True
     # if not format_helper.validate_input("integer",input.job_id):
     #     ErrorMessage += 'Job Id has characters that are not intergers'
     #     return_value= False
     #
     # if not format_helper.validate_input("date",input.date_time):
     #     ErrorMessage += 'Date input field is not in the correct format'
     #     return_value=False

     if input.status.lower() == 'started':
         if not insert_staterd_job(input):
             ErrorMessage += "An error occured whileinserting record int the DynamoDb"
             return False
     else:
         if record_exists(input.job_id):
             if update_completed_or_failed_job(input):
                return_value = True
             else:
                 ErrorMessage += 'An error occured while trying to update an existent record on the DynamoDb'
                 return False
         else:
             ErrorMessage += 'An error occured while trying to update a non existent record on the DynamoDb'
     return return_value


def insert_staterd_job(input):
    global ErrorMessage
    try:
        client.put_item(
            TableName=Notification_Table,
            Item={
                'JobId': {'S': input.job_id},
                'ClientId': {'S': input.client_id},
                'JobStatus': {'S': input.status},
                'startime': {'S': input.date_time},
                'endtime': {'S':""},
                'MetaData': {'S': input.metadata},
            }
        )
    except  Exception as x:
         ErrorMessage +='An error occure while attempting to insert the beginning of a job into the Dynamo Db'
         return False
    return True


def update_completed_or_failed_job(input):

    try:
        response = client.update_item(
            TableName=Notification_Table,
            Key={
                'JobId': input,
            },
            UpdateExpression="set info.endtime=:r, infor.JobStatus=:a",
            ExpressionAttributeValues={
                ':r': input.date_time,
                ':a': input.status
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as ex:
        return False
    return True

def get_duration_for_failed_or_completed_jobs(jobId,enddate):
     response = get_item_by_JobId(jobId)
     return datetime.strptime(enddate,'%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(response['Item']['startime'],'%Y-%m-%d %H:%M:%S.%f')


def record_exists(jobId):
    try:

        response = client.get_item(TableName=Notification_Table,Key={'JobId':jobId})
    except ClientError as e:
        return False
    return True


def get_item_by_JobId(jobId):
    response = client.get_item(TableName=Notification_Table,Key={'JobId':jobId})
    return response