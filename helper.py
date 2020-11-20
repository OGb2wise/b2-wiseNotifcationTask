
import json
import os
import format_helper
import types


bad_request=400
ok = 200
unauthorised= 401
internal_server_error = 500
authKey = os.environ['authorizationKey']

class InputData:
    def __init__(self):
        self.job_id = 0
        self.client_id= 0
        self.processing_region=""
        self.message=""
        self.status=""
        self.date_time= ""
        self.metadata=""




def formatResponse(message,status):
    return {
        'statusCode': status,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(message)
    }


def validate_sqs_queue(event):
    if 'Records' not in event:
        return formatResponse('The sqs message is empty',bad_request)
    for record in event['Records']:
        if not validate_key('attributes',record):
            return formatResponse('some messages missing attributes',bad_request)
        if not validate_metadata(record):
            return formatResponse('some messages do not contain metadata',bad_request)
        if not validate_key_with_value('authorization',record,authKey):
            return formatResponse('authorization failed',unauthorised)
        if not validateResonse(record['attributes'],True):
            return formatResponse('some attributes are missing',bad_request)
        if not validate_status(record['attributes']):
            return formatResponse('Invalid status Type',bad_request)
    return formatResponse('Validation passed',ok)


def validateResonse(event,exclude_body):
    if not exclude_body:
        return validate_key_list(['queryStringParameters','body'],event)
    else:
        return validate_key_list(['queryStringParameters'],event)

def checkQueryString(event):
    return 'queryStringParameters' in event.keys()


def validate_parameters(event):
   return validate_key_list(['jobid','clientid','status','datetime','processingregion'],event)


def validate_key_list(keylist,event):
    return len([i for i in keylist if is_key_in_event(i,event) ]) == len(keylist)

def authorize(event):
    if not validate_key('headers',event):
        return formatResponse("The request does not have headers", bad_request)
    header = event['headers']
    if not validate_key_with_value('authorization',header,authKey):
        return formatResponse('Authorization failed',unauthorised)
    return formatResponse("validation Passed",ok)

def validate_key(key,event):
    return  is_key_in_event(key.lower(),event) or  is_key_in_event(key.upper(),event) or  is_key_in_event(key.capitalize(),event)


def validate_key_with_value(key,event,value):
    if not validate_key(key,event):
        return False
    if is_key_in_event(key.lower(),event):
       return event[key.lower()]==value
    if is_key_in_event(key.upper(),event):
       return event[key.upper()]==value
    if is_key_in_event(key.upper(),event):
       return event[key.capitalize()]==value


def is_key_in_event(key,event):
    return key in event.keys()

def extract_value_by_key(key,event):
    try:
          return event[key.lower()]
    except:
        try:
            return event[key.upper()]
        except:
            return event[key.capitilize()]
    raise Exception(
        'Attempted to extract a nonExistent keu from a dictionary')

def validate_response(event):
    if not validateResonse(event,False):
        return formatResponse("The request did not pass validation",bad_request)
    if not validate_status(event['queryStringParameters']):
        return formatResponse("Invalid Job status",bad_request)
    return authorize(event)


def create_request(input,event):
    request = InputData()
    request.job_id = input['jobid']
    request.date_time = input['datetime']

    request.status = input['status']
    if 'message' in input.keys():
     request.message = input['message']
    request.client_id = input['clientid']
    if is_string_valid_jason(event['body']['metadata']):
     request.metadata = json.dumps(event['body']['metadata'])
    request.processing_region = input['processingregion']
    return request

def create_request_sqs(input,event):
    request = InputData()
    request.job_id = input['jobid']
    request.date_time = input['datetime']
    request.status = input['status']
    if 'message' in input.keys():
     request.message = input['message']
    request.client_id = input['clientid']
    if is_string_valid_jason(event['body']['metadata']):
     request.metadata = json.dumps(event['body']['metadata'])
    request.processing_region = input['processingregion']
    return request


def is_string_valid_jason(input):
    try:
       json.loads(input)
    except:
        return False
    return True

def validate_status(input):
    return input['status'].lower()=="started" or input['status'].lower()=="failed" or input['status'].lower()=="completed"

def validate_time_format(input):
    return format_helper.is_valid_date_time(input['time'])

def validate_metadata(input):
    try:
        result = is_key_in_event('metadata',input['body'])
        return result
    except:
        return False


def boolean_based_response(snsStatus,dynamoDbStatus):
    if not snsStatus and not dynamoDbStatus:
        return formatResponse("An error occured while writting data to Dymnamo Db and publishing a message to sns",
                              internal_server_error)
    if not dynamoDbStatus:
        return formatResponse("An error occured while writting data to Dymnamo Db ",
                               internal_server_error)
    if not snsStatus:
        return formatResponse("An error occured while publishing a message to sns",
                              internal_server_error)

    return formatResponse( "process notification generated successfully",
                           internal_server_error)