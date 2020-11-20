import boto3
import helper



def format_request(request):
     message = ""
     if request.status.lower() == "failed":
         message += "Job Id:\t" + str(request.job_id)  + "\twith Client ID :\t"+str(
             request.client_id)+ "\t" + request.status + "\tat\t"+request.date_time + "\twith the following message"+request.message

     else:
         message += "Job Id:\t" + str(request.job_id) + "\twith Client ID :\t" + str(
             request.client_id) + "\t" + request.status + "\tat\t" + request.time
     return message


def publish_sns_message(topic_arn,request):
         if not isinstance(request, helper.InputData):
             return False
         sns = boto3.client('sns')
         sns_response = sns.publish(
             TopicArn=topic_arn,
             Message=format_request(request),
             Subject="Job Notification"
         )
         return True


