import unittest

from cloudformation_logs_to_slack import app


class context:
    def __init__(self):
        pass

class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.test_sns_event_with_delete_in_progress = {
            "Records": [
                {
                    "EventSource": "aws:sns",
                    "EventVersion": "1.0",
                    "EventSubscriptionArn": "arn:aws:sns:ap-southeast-2:xxx:sns-cloudformation:zzzz",
                    "Sns": {
                        "Type": "Notification",
                        "MessageId": "e90664ad-c5b2-58c2-8c1d-3149e416d1df",
                        "TopicArn": "arn:aws:sns:ap-southeast-2:xxx:sns-cloudformation",
                        "Subject": "AWS CloudFormation Notification",
                        "Message": "StackId='arn:aws:cloudformation:ap-southeast-2:xxx:stack/test/aff99e20-cbbd-11e9-8b76-0613a29612d8'\nTimestamp='2019-08-31T07:19:00.310Z'\nEventId='9a86ac20-cbbf-11e9-9b10-024486204d54'\nLogicalResourceId='test'\nNamespace='xxx'\nPhysicalResourceId='arn:aws:cloudformation:ap-southeast-2:xxx:stack/test/aff99e20-cbbd-11e9-8b76-0613a29612d8'\nPrincipalId='xxxx'\nResourceProperties='null'\nResourceStatus='DELETE_IN_PROGRESS'\nResourceStatusReason='User Initiated'\nResourceType='AWS::CloudFormation::Stack'\nStackName='test'\nClientRequestToken='null'\n",
                        "Timestamp": "2019-08-31T07:19:00.365Z",
                        "SignatureVersion": "1",
                        "Signature": "D61n84tlfRRJkO8qi27GaiRHV0Eozwq3WmB4M1YAXH5VPe+DVmyDxtrPcPPHFTEZ2ga9Wg6ndokqUiEle/5dhykeJFoQWxxv60L4dcD5XNmipsxAdjTdAjNNvDIZ1sJZukTcsK7DN9g3obRz+qCtfStEUWPG4OsghEtJ1SAORwFDKnCesm1D3cBOvi96LBFBqGJzDnBmAtd2KmTVkGAvUoshf4QsnpIsJ37eCgQhQMoLg3gzFeNwjHsnjQMnTrgw0Wqs6W3mNhOEqnyOFD03ZN3dKS4OWd8QMYhYuOXyY+Zx3rMy7+Zbq6GpjVLZNRmYGAqTxo0vWYCZ21u/s2pwww==",
                        "SigningCertUrl": "https://sns.ap-southeast-2.amazonaws.com/SimpleNotificationService-yyyy.pem",
                        "UnsubscribeUrl": "https://sns.ap-southeast-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ap-southeast-2:xxx:sns-cloudformation:zzzz",
                        "MessageAttributes": {}
                    }
                }
            ]
        }

    def test_record_event_to_dict(self):
        """Test the record_event_to_dict method"""
        
        # act
        result = app.record_event_to_dict(self.test_sns_event_with_delete_in_progress["Records"][0])

        # assert
        self.assertTrue(result["ResourceStatus"] == "DELETE_IN_PROGRESS")
