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

    # You must create the connectorcard object with the Microsoft Webhook URL
    # notification = pymsteams.connectorcard(webhook_url)
    # notification.title("{}: {} {}".format(notification_type,event_detail['eventTypeCategory'], event_detail['eventTypeCode']))
    # notification.summary(event_detail['service'])
    #
    # healthevent_section = pymsteams.cardsection()
    # healthevent_section.activityTitle(event_detail['service'])
    # healthevent_section.text(event_detail['eventDescription'][0]['latestDescription'])
    # healthevent_section.addFact("Region", event['region'])
    # healthevent_section.addFact("Started on", event_detail['startTime'])
    # healthevent_section.addFact("Ended on", event_detail['endTime'])
    # healthevent_section.activityImage(img.health)
    #
    # notification.addSection(healthevent_section)
    # notification.printme()


    return {
        "message": "Function executed successfully!",
        "event": event
    }

