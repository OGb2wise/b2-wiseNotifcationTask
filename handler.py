import json

import helper
import sns_publisher
import os

import Data_writter

Notification_Table = os.environ['Notification_Table']
SNS_ARN = os.environ['snsarn']


def api_notify(event, context):
    #test deployment
    validation = helper.validate_response(event)
    if validation['statusCode']!=200:
        return validation
    validatedrequest = helper.create_request(event['queryStringParameters'],event)
    sns_status = sns_publisher.publish_sns_message(SNS_ARN,validatedrequest)
    dynamoDbStatus = Data_writter.write_data(validatedrequest)
    return helper.boolean_based_response(sns_status, dynamoDbStatus)



def  sqs_notify(event,context):
     validation = helper.validate_sqs_queue(event)
     if validation['statusCode'] != 200:
         return validation
     for record in event['Records']:
         validatedrequest = helper.create_request_sqs(record['attributes'],record)
         sns_publisher.publish_sns_message(SNS_ARN,validatedrequest)
         Data_writter.write_data(validatedrequest)
     return helper.formatResponse('Messages sent to DynamoDb and Sns successfully',helper.ok)