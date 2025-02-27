from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

# Define the basic cluster body structure outside the function
cluster_body = {
    "initial_cluster_version": "latest",
    "node_pools": [{"name": "default-pool"}]  # Default node pool
}


def create_gke_cluster(project_id, location, cluster_name, basic_config, additional_config=None):
    """Creates a GKE cluster.

    Args:
        project_id: The Google Cloud Project ID.
        location: The zone or region for the cluster.
        cluster_name: The name of the cluster.
        basic_config: Basic cluster configuration dictionary.
        additional_config: Optional additional configuration.

    Returns:
        Operation details if successful, raises HttpError otherwise.
    """

    credentials = GoogleCredentials.get_application_default()
    container = discovery.build('container', 'v1', credentials=credentials)

    # Update the node pool configuration
    cluster_body["node_pools"][0].update(basic_config)  #Apply basic config to default pool
    if additional_config:
        cluster_body["node_pools"][0].update(additional_config)


    # Set the cluster name in the body
    cluster_body["name"] = cluster_name

    request = container.projects().locations().clusters().create(
        parent=f"projects/{project_id}/locations/{location}",
        body=cluster_body
    )

    try:
        response = request.execute()
        return response
    except HttpError as e:
        print(f"Error creating cluster: {e}")
        raise




# Example usage:
project_id = input("Enter your project ID: ")
location = input("Enter the location (zone or region): ")
cluster_name = input("Enter the desired cluster name: ")

basic_config = {
    "initial_node_count": 2,
    "node_config": {
        "machine_type": "e2-medium",
        "disk_size_gb": 50
    }
}

additional_config = {  # Example (optional)
    "network": "projects/" + project_id + "/global/networks/your-network-name", # Update network name
    "subnetwork": "projects/" + project_id + "/regions/your-region/subnetworks/your-subnetwork-name",  # Update subnetwork name and region
    "node_config": {
        "disk_size_gb": 100,
        "labels": {"env": "dev", "team": "platform"}
    }
}

try:
    operation = create_gke_cluster(project_id, location, cluster_name, basic_config, additional_config)
    print(f"Cluster creation started. Operation details: {operation}")
except HttpError as e:
    print(f"Cluster creation failed.")

