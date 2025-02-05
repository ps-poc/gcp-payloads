


from google.oauth2 import service_account
from googleapiclient.discovery import build





import google.auth
import random
# from oauth2client.client import GoogleCredentials
import logging
logger = logging.getLogger(__name__)
import re
from google.oauth2 import service_account
from google.auth import impersonated_credentials, default
from googleapiclient.discovery import build
import time

class MonitoringServiceV3:

    def __init__(self) -> None:
        # credentials = GoogleCredentials_getapplication_default()
        # credentials, project_id = google.auth.default()

        target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        source_credentials, _ = default()

        self.target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal='bhakti-sa@prj-se-bhachikh-3fec.iam.gserviceaccount.com',
            target_scopes=target_scopes,
            lifetime=500)
        self.monitoring_service_v3 = build('monitoring', 'v3', credentials=self.target_credentials)
        self.project_id= 'prj-se-bhachikh-3fec'

    def create_alert_policies(self):
        body = {
            "notificationChannels": [
                "projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215"
                
            ],
            "displayName": "testing-alertpolicy-displayname",
            "conditions": [
                {
                "conditionThreshold": {
                    "thresholdValue": 0.2,
                    "filter": "resource.type = \"gce_instance\" OR metric.type = \"compute.googleapis.com/instance/cpu/usage_time\"",
                    "comparison": "COMPARISON_GT",
                    "duration": "0s"
                    
                },
                "displayName": "VM Instance - CPU usage"
                
                }
                
            ],
            "combiner": "AND"
            
            }
        try:
            request = self.monitoring_service_v3.projects().alertPolicies().create(
                name=f'projects/{self.project_id}',
                body=body
            )
            response = request.execute()

            print("alert policies added successfully resp:\n", response)
        except Exception as e:
            print("An error occurred while adding alert policies:\n", e)


if __name__ == '__main__':
    
    cs = MonitoringServiceV3()
    project_id = 'prj-se-ravavula-8fcb'
    # project_id='prj-se-chedewan1-21ca'
    parent_metrics_scope = 'prj-se-bhachikh-3fec'
    resp=cs.create_alert_policies()
    print(resp)

# <HttpError 400 when requesting https://monitoring.googleapis.com/v3/projects/prj-se-bhachikh-3fec/alertPolicies?alt=json returned "Field alert_policy.notification_channels[0] had an invalid value of "projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215": Project "prj-se-pankaj-54e7" in the channel name ("projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215")does not match the request's project of "prj-se-bhachikh-3fec" (#664869673844).". Details: "Field alert_policy.notification_channels[0] had an invalid value of "projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215": Project "prj-se-pankaj-54e7" in the channel name ("projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215")does not match the request's project of "prj-se-bhachikh-3fec" (#664869673844).">


#{
#   "error": {
#     "code": 400,
#     "message": "Field alert_policy.notification_channels[0] had an invalid value of \"projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215\": Project \"prj-se-pankaj-54e7\" in the channel name (\"projects/prj-se-pankaj-54e7/notificationChannels/9151909956153220215\")does not match the request's project of \"prj-se-bhachikh-3fec\" (#664869673844).",
#     "status": "INVALID_ARGUMENT"
#   }
# }
