import event_images
import pymsteams



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

    if source == "aws.signin":
        notification_section = signin_notification(detail_type, event_detail)
    elif source == "aws.health":
        notification_section = health_notification(detail_type, event_detail)
    elif source == "aws.guardduty":
        notification_section = guardduty_notification(detail_type, event_detail)
    elif source == "aws.codepipeline":
        notification_section = codepipeline_notification(detail_type, event_detail)
    else:
        notification_section = default_notification(detail_type, event_detail)

    cwe_notification.addSection(notification_section)

    cwe_notification.send()

def default_notification(detail_type, event_detail):
