import event_images


def notify_event(type, event_detail):
    '''
        Entry function for all events

        Supported Events:
            - AWS Console Signins
            - GuardDuty Findings
            - Health Events
            - Codepipeline execution changes
    '''

    
