import sys

sys.path.append("/opt")

import logging
import pymsteams
import os

# import requests

# Define A logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

webhook_url = os.environ.get("MSTEAMS_WEBHOOK_URL")

def lambda_handler(event, context):
    logger.info('Event: {}'.format(event))
    notification_type = "AWS Health"
    event_detail = event['detail']


    # You must create the connectorcard object with the Microsoft Webhook URL
    notification = pymsteams.connectorcard(webhook_url)
    notification.title("{}: {} {}".format(notification_type,event_detail['eventTypeCategory'], event_detail['eventTypeCode']))
    notification.summary(event_detail['service'])

    healthevent_section = pymsteams.cardsection()
    healthevent_section.activityTitle(event_detail['service'])
    healthevent_section.text(event_detail['eventDescription'][0]['latestDescription'])
    healthevent_section.addFact("Region", event['region'])
    healthevent_section.addFact("Started on", event_detail['startTime'])
    healthevent_section.addFact("Ended on", event_detail['endTime'])

    notification.addSection(healthevent_section)
    notification.printme()
    notification.send()

    return {
        "message": "Function executed successfully!",
        "event": event
    }

