


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
from google.cloud import compute_v1
import time

class MonitoringService:

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
        self.monitoring_service = build('monitoring', 'v1', credentials=self.target_credentials)
        # self.project_id= 'prj-se-bhachikh-3fec'
        # locations/global/metricsScopes/prj-se-bhachikh-3fec/projects/prj-se-workspace-9f7a

    def add_monitored_project(self, parent_metrics_scope, project_id):

        monitored_project_body = {
            'name': f'locations/global/metricsScopes/{parent_metrics_scope}/projects/{project_id}'
        }
        try:
            request = self.monitoring_service.locations().global_().metricsScopes().projects().create(
                parent=f'locations/global/metricsScopes/{parent_metrics_scope}',
                body=monitored_project_body
            )
            response = request.execute()

            print("Monitored Project added successfully resp:\n", response)
        except Exception as e:
            print("An error occurred:", e)

    def delete_monitored_project(self, parent_metrics_scope, project_id):

        try:
            request = self.monitoring_service.locations().global_().metricsScopes().projects().delete(
                name=f'locations/global/metricsScopes/{parent_metrics_scope}/projects/{project_id}'
            )
            response = request.execute()

            print("Monitored Project deleted successfully resp:\n", response)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == '__main__':
    
    cs = MonitoringService()
    project_id = 'prj-se-ravavula-8fcb'
    # project_id='prj-se-chedewan1-21ca'
    parent_metrics_scope = 'prj-se-bhachikh-3fec'
    # resp = cs.add_monitored_project(parent_metrics_scope, project_id)
    resp = cs.delete_monitored_project(parent_metrics_scope, project_id)
    print(resp)

    # pattern = r'locations/global/metricsScopes/([^/]+)/projects/([^/]+)'

    # # Use re.search to find the match in the string
    # match = re.search(pattern, "locations/global/metricsScopes/prj-se-bhachikh-3fec/projects/prj-se-chedewan1-21ca")
    
    # if match:
    #     # Extract the IDs
    #     scoping_project_id = match.group(1)
    #     monitored_project_id = match.group(2)
    #     print(scoping_project_id)
        # print(monitored_project_id)
