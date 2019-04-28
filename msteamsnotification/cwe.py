import event_images
import pymsteams
import json

class CloudWatchEvent:
    def __init__(self, event):
        self.title = event["detail-type"]
        pass

    def deliver_to_channels(self, webhook_urls):
        pass

def notification(webhook_url, source, detail_type, event_detail):
    '''
        Entry function for all events

        Supported Events:
            - AWS Console Signins
            - GuardDuty Findings
            - Health Events
            - Codepipeline execution changes
    '''
    cwe_notification = pymsteams.connectorcard(webhook_url)
    cwe_notification.title(detail_type)
    cwe_notification.summary(f"{source}: {detail_type}")

    if source == "aws.signin1":
        notification_section = signin_notification(detail_type, event_detail)
    elif source == "aws.health1":
        notification_section = health_notification(detail_type, event_detail)
    elif source == "aws.guardduty1":
        notification_section = guardduty_notification(detail_type, event_detail)
    elif source == "aws.codepipeline1":
        notification_section = codepipeline_notification(detail_type, event_detail)
    else:
        notification_section = default_notification(detail_type, event_detail)

    cwe_notification.addSection(notification_section)

    cwe_notification.send()


def default_notification(detail_type, event_detail):
    section = pymsteams.cardsection()
    parse_facts(details=event_detail, section=section)

    return section


def signin_notification(detail_type, event_detail):
    pass


def health_notification(detail_type, event_detail):
    pass


def guardduty_notification(detail_type, event_detail):
    pass


def codepipeline_notification(detail_type, event_detail):
    pass


def parse_facts(details, section, keys=None):
    for detail in details:
        if type(detail) is str:
            section.addFact(detail, details[detail])
        else:
            parse_facts(details[detail])