import sys

sys.path.append("/opt")

import logging
import os
import cwe

# import requests

# Define A logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

WEBHOOK_URL = os.getenv("MSTEAMS_WEBHOOK_URL", "none")
# Notify on SNS topic or CWE Event
NOTIFICATION_TYPE = os.getenv("NOTIFICATION_TYPE", "cwe").lower()


def lambda_handler(event, context):
    logger.info('Event: {}'.format(event))

    if WEBHOOK_URL == "none":
        logger.error("Webhook not defined!")
        return {
            "message": "Failure!"
        }

    if NOTIFICATION_TYPE == "cwe":
        notification = cwe.CloudWatchEvent(event)
    if NOTIFICATION_TYPE == "sns":
        pass

    notification.deliver_to_msteams_channel(WEBHOOK_URL)

    return {
        "message": "Function executed successfully!",
        "event": event
    }

