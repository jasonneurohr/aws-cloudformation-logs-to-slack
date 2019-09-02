import logging
import requests

from json import dumps
from os import getenv

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_notification(message: str = None, timestamp: str = "", color: str = "good"):
    """Sends a notification to Slack

    Slack API Documentation for attachments - https://api.slack.com/docs/message-attachments

    :param message: The Slack message text
    :param timestamp: The timestamp for the cloudwatch event
    :param color: Attachment color, 'good', 'warning', 'danger', or a hex code e.g. '#439FE0'
    """

    slack_uri = getenv("SLACK_WEBHOOK")

    attachment = dict(
        {
            "attachments": [
                {
                    "title": f"Cloudformation Event - {timestamp}",
                    "text": message,
                    "color": color,
                }
            ]
        }
    )

    req_data = dumps(attachment)

    req_headers = {"Content-type": "application/json"}
    req = requests.post(url=slack_uri, headers=req_headers, data=req_data)


def record_event_to_dict(event_record: str = None):
    """Takes a event record and breaks it up into a dictinary with the following keys
    
    "StackId"
    "Timestamp"
    "EventId"
    "LogicalResourceId"
    "Namespace"
    "PhysicalResourceId"
    "PrincipalId"
    "ResourceProperties"
    "ResourceStatus"
    "ResourceStatusReason"
    "ResourceType"
    "StackName"
    "ClientRequestToken"
    
    :param record_event: a string record event
    :returns dict: a dict of the record event
    """

    msg_dict = {}

    cf_event_message = event_record["Sns"]["Message"]
    for line in cf_event_message.split("\n"):
        line = line.replace("'", "")
        logger.info(f"line: {line}")
        if line.find("=") >= 0:
            bits = line.split("=")
            msg_dict[bits[0]] = bits[1]

    logger.debug(f"event_record dict: {dumps(msg_dict)}")

    return msg_dict


def lambda_handler(event, context):
    logger.info(f"lambda_handler entered")
    logger.debug(f"Log Events: {dumps(event)}")

    for record in event["Records"]:
        record_dict = record_event_to_dict(record)

        stack_name = record_dict["StackName"]
        timestamp = record_dict["Timestamp"]
        logical_resource_id = record_dict["LogicalResourceId"]
        resource_status = record_dict["ResourceStatus"]
        resource_status_reason = record_dict["ResourceStatusReason"]
        resource_type = record_dict["ResourceType"]

        alert_msg = f"StackName: {stack_name}\n"
        alert_msg += f"ResourceStatus: {resource_status}\n"
        alert_msg += f"LogicalResourceId: {logical_resource_id}\n"
        alert_msg += f"ResourceStatusReason: {resource_status_reason}\n"
        alert_msg += f"ResourceType: {resource_type}\n"

        if resource_status == "CREATE_FAILED":
            send_notification(message=alert_msg, timestamp=timestamp, color="danger")
        elif (
            resource_status == "UPDATE_ROLLBACK_IN_PROGRESS"
            or resource_status == "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS"
            or resource_status == "UPDATE_ROLLBACK_COMPLETE"
        ):
            send_notification(message=alert_msg, timestamp=timestamp, color="warning")
        elif (
            resource_status == "CREATE_IN_PROGRESS"
            or resource_status == "DELETE_IN_PROGRESS"
        ):
            send_notification(message=alert_msg, timestamp=timestamp, color="#439FE0")
        else:
            send_notification(message=alert_msg, timestamp=timestamp)
