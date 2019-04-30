import event_images
import pymsteams
import json
import json_util


class CloudWatchEvent:
    def __init__(self, event):
        self.title = event["detail-type"]
        self.account_id = event["account"]
        self.region = event["region"]
        self.resources = event["resources"]

        if event["source"] in ["aws.health", "aws.signin", "aws.codepipeline"]:
            # This will parse the details we want
            self._parse_details(event["detail"], event["source"])
        else:
            # We take everything and flatten it a single level
            self.data = flatten_json(event["detail"])

    def _parse_details(self, event_detail, event_source):
        data = {}

        if event_source == "aws.health":
            self.title = f"{event_detail['service']} - {event_detail['eventTypeCode']} ({event_detail['eventTypeCategory']})"
            self.subtitle = f"{event_detail['eventArn']}"
            self.image = event_images.health
            self.data = {
                "Started On": event_detail['startTime'],
                "Ended On": event_detail['endTime'],
                "description": fetch_translation(event_detail['eventDescription'], 'en_US')['latestDescription']
            }
        elif event_source == "aws.signin":
            self.title = f"{event_detail['eventName']} :: {event_detail['awsRegion']} : {event_detail['userIdentity']['accountId']} - {event_detail['responseElements']['ConsoleLogin']}"
            self.subtitle = f"{event_detail['eventTime']}"
            self.image = event_images.signin
            self.data = {
                "identity-type": event_detail['userIdentity']['type'],
                "identity-principal-id": event_detail['userIdentity']['principalId'],
                "identity-principal-arn": event_detail['userIdentity']['arn'],
                "source-ip": event_detail['sourceIPAddress'],
                "user-agent": event_detail['userAgent'],
                "mfa-user": event_detail['additionalEventData']['MFAUsed']
            }
        # elif event_source == "aws.guardduty":
        #     self.title = f""
        #     self.subtitle = f""
        #     self.image = event_images.signin
        #     self.data = {}
        # elif event_source == "aws.codepipeline":
        #     self.title = f""
        #     self.subtitle = f""
        #     self.image = event_images.signin
        #     self.data = {}

    def deliver_to_msteams_channel(self, channel_url):
        notification = pymsteams.connectorcard(channel_url)
        notification.title(self.title)
        notification.summary(f"{self.title} - {self.subtitle}")
        section = pymsteams.cardsection()
        section.activityTitle(self.subtitle)
        section.activityImage(self.image)
        for key, value in self.data.items():
            section.addFact(key, value)
        notification.addSection(section)
        notification.printme()
        notification.send()

    # NotYetImplemented
    #def deliver_to_slack_channels(self, webhook_urls):
    #    pass


def fetch_translation(lang_list, lang):
    for language_object in lang_list:
        if language_object['language'] == lang:
            return language_object

    return lang_list[0]
