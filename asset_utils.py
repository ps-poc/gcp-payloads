import logging
from typing import Optional
from googleapiclient import discovery
from common.base_utils import BaseUtils
import time
from google.cloud import dlp_v2
import datetime

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

QUOTA_PROJECT = "prj-c-localloop-e040"

PARENT_NAME = "organizations/prj-se-madkumar4-b082/environments/test-env"

NAME =f"test_{time.time()}"

class AssetDiscoveryUtils():

    def get_service(self):
        return discovery.build("apigee","v1")
    
    def search_resource_in_asset_inventory(self,organization_id, asset_types, resource_name) -> str:
        results = []
        service = discovery.build("cloudasset", "v1")
        try:
            request = service.v1().searchAllResources(
                scope=f"organizations/{organization_id}",
                assetTypes=asset_types,
                query=f"name:{resource_name}",
                readMask="name",
            )
            response = request.execute()

            if response is not None and "results" in response:
                results = response["results"]
        except Exception as ex:
            print(ex)

        return results
    
    def asset_list_inventory(self,parent_path, asset_types, timestamp) -> str:
        results = []
        service = discovery.build("cloudasset", "v1")
        try:
            request = service.assets().list(
                parent=parent_path,
                assetTypes=asset_types,
                contentType='RESOURCE',
                readTime=timestamp
            )
            response = request.execute()

            if response and "assets" in response:
                results = response["assets"]
                print(f"read Time : {response['readTime']}")
        except Exception as ex:
            print(ex)

        return results

    
    def create_target_server(self):
        payload = {
            "name" :NAME,
            "host" : "github.com",
            "port":2
        }
        request = self.get_service().organizations().environments().targetservers().create(parent = PARENT_NAME,body=payload)
        response = request.execute()
        print(f"Created server : {response}")
    
    def update_target_server(self,name):
        payload = {
            "host" : "github.com",
            "port":5,
            "sSLInfo": {
                 "enabled": True,
                 "ignoreValidationErrors":True
            }
        }
        request = self.get_service().organizations().environments().targetservers().update(name = PARENT_NAME+"/targetservers/"+name,body=payload)
        response = request.execute()
        print(f"Updated server : {response}")

    def get_target_server(self,name):
        request = self.get_service().organizations().environments().targetservers().get(name = PARENT_NAME+"/targetservers/"+name)
        response = request.execute()
        print(f"Get server : {response}")

    def list_target_server(self):
        request = self.get_service().organizations().environments().targetservers().list(parent = PARENT_NAME)
        response = request.execute()
        print(f"List server : {response}")

    # 829664665525 project id
    # 935878585818 org id
    def is_check_resource_name_exist(self):
        results = self.search_resource_in_asset_inventory(
                "935878585818", ["apigee.googleapis.com/Organization"], "prj-se-madkumar4-b082"
            )
        print(f"results : {results}")
        
    def delete_target_server(self):
        request = self.get_service().organizations().environments().targetservers().delete(name = PARENT_NAME+"/targetservers/"+NAME)
        response = request.execute()
        print(f"Delete server : {response}")

    def read_logs(self,project_id,service_name, method_name, resource_name):
        logging_service = discovery.build("logging", "v2")
        # Step 4: Define time range for log query (e.g., the 30 days)
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=30)
        # Convert to RFC3339 format
        start_time_rfc = start_time.isoformat() + "Z"
        end_time_rfc = end_time.isoformat() + "Z"
        log_filter = f'''protoPayload.serviceName="{service_name}" 
        AND protoPayload.methodName="{method_name}" 
        AND protoPayload.resourceName="{resource_name}" 
        AND protoPayload.request.targetServer.host="github.com" 
        AND timestamp >= "{start_time_rfc}" AND timestamp <= "{end_time_rfc}"
        AND severity!="ERROR" ''' 
        # Step 5: Define filter to read logs from the last 30 days
        print(f"Search filter duration : {log_filter}")
        try:
            # List log entries with filter
            payload ={
                "projectIds": [project_id],
                "filter":log_filter,
                "orderBy":"timestamp desc",
                "pageSize":5
            }
            entries = logging_service.entries().list(body=payload).execute()
        
            # Process the logs and print them
            for entry in entries.get('entries', []):
                print(f"Log Name: {entry.get('logName')}")
                print(f"Severity: {entry.get('severity')}")
                print(f"Timestamp: {entry.get('timestamp')}")
                print(f"Text Payload request: {entry.get('protoPayload').get('request')}")
                print(f"Text Payload response: {entry.get('protoPayload').get('request')}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    assert_utils = AssetDiscoveryUtils()

    results = assert_utils.search_resource_in_asset_inventory(
                "935878585818", ["apigee.googleapis.com/Organization"], "target_servername"
            )
    
    #assert_utils.update_target_server("test_1738838612.8802938")
    #assert_utils.get_target_server("test_1738838612.8802938")
    #assert_utils.is_check_resource_name_exist()
    #assert_utils.read_logs('prj-se-madkumar4-b082','apigee.googleapis.com',
    #                       'google.cloud.apigee.v1.TargetServerService.UpdateTargetServer',
    #                       'organizations/prj-se-madkumar4-b082/environments/test-env/targetservers/test_1738838612.8802938')

    ''' 
    assert_utils.create_target_server()
    name = assert_utils.update_target_server(NAME)
    
    assert_utils.list_target_server()
    assert_utils.get_target_server(NAME)
    assert_utils.delete_target_server()
    '''