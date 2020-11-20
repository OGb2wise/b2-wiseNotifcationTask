import boto3
import helper
import data_writter



def format_request(request):
     message = ""
     duration = ""
     if request.status.lower() == "failed" or request.status.lower() == "completed" :
         if data_writter.record_exists(request.job_id):
            duration += str(data_writter.get_duration_for_failed_or_completed_jobs(request.job_id, request.date_time))
         message += "Job Id:\t" + str(request.job_id)  + "\twith Client ID :\t"+str(
             request.client_id)+ "\t" + request.status + "\tat\t"+request.date_time + "\t Duration was: \t" + str(duration)

     else:
         message += "Job Id:\t" + str(request.job_id) + "\twith Client ID :\t" + str(
             request.client_id) + "\t" + request.status + "\tat\t" + request.date_time
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


