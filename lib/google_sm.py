
from google.cloud import secretmanager

class SecretManagerUtil:
    def get_secret(self, secret_id: str, project_id: str = "233526485971") -> str:
        """
        Default: project_id: selen-autopurchase GCPプロジェクト
        """
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")