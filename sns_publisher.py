import boto3
import helper
import Data_writer



def format_request(request):
     message = ""
     duration = ""
     if request.status.lower() == "failed" or request.status.lower() == "completed" :
         if Data_writer.record_exists(request.job_id):
            duration += Data_writer.get_duration_for_failed_or_completed_jobs(request.job_id,request.time)
         message += "Job ID: " + str(request.job_id)  + " with Client ID : "+str(
             request.client_id)+ " " + request.status + " at "+request.date_time + " UTC.\nDuration: " + str(duration) +
             "\nProcessing region: " + request.processing_region

     else:
         message += "Job ID: " + str(request.job_id) + " with Client ID : " + str(
             request.client_id) + " " + request.status + " at " + request.date_time + " UCT." +
             "\nProcessing region: " + request.processing_region
     return message


def publish_sns_message(topic_arn,request):
         if not isinstance(request, helper.InputData):
             return False
         sns = boto3.client('sns')
         sns_response = sns.publish(
             TopicArn=topic_arn,
             Message=format_request(request),
             Subject="Notification"
         )
         return True


