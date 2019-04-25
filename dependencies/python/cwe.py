import event_images
import pymsteams



def create_notification_card(source, detail_type, event_detail):
    '''
        Entry function for all events

        Supported Events:
            - AWS Console Signins
            - GuardDuty Findings
            - Health Events
            - Codepipeline execution changes
    '''

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

    return notification_section

def default_notification(detail_type, event_detail):
