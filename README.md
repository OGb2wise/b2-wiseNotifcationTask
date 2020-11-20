# Notification Service

An Event Monitoring Notification Service that receives input from an Amazon SQS (Simple Queue Service) or through Amazon API Gateway, triggers an AWS Lambda function, then outputs to Amazon DynamoDB, Amazon SNS (Amazon Simple Notification Service) and Prometheus (https://prometheus.io/).


## Architecture:
!("C:\Users\JadineKruger\Downloads\notification_service.png")

## Endpoints:

Method | Path
------------ | -------------
post | /

### Input:

Source | Field | Required | Data Type
------------ | ------------- | ------------- | -------------
Query Parameter | jobid | Yes | String
Query Parameter | clientid | Yes | String
Query Parameter | processingregion | Yes | String
Query Parameter | status | Yes | "started", "completed", "failed"
Query Parameter | environment | Yes | String
Query Parameter | time | Yes | String representation of a datetime object.<br>Either:<br>year-month-day hour:minute:second.microsecond<br>'%Y-%m-%d %H:%M:%S.%f'<br>OR<br>year/month/day hour:minute:second.microsecond<br>'%Y/%m/%d %H:%M:%S.%f'
Query Parameter | errors | No | String
Body | metadata | Yes | JSON
