import os
import requests
import msal
import yaml
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

def load_app_role_mapping(path="app_role_mapping.yaml"):
       with open(path) as f:
           config = yaml.safe_load(f)
       return config["apps"]

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return result["access_token"]

def assign_app_role_to_group(token, group_id, service_principal_id, app_role_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/appRoleAssignments"

    # Idempotency check — same pattern as your group script
    existing = requests.get(url, headers=headers).json()
    for assignment in existing.get("value", []):
        if assignment["appRoleId"] == app_role_id and assignment["resourceId"] == service_principal_id:
            print("Role already assigned — skipping.")
            return

    body = {
        "principalId": group_id,
        "resourceId": service_principal_id,
        "appRoleId": app_role_id,
    }
    resp = requests.post(url, headers=headers, json=body)
    if resp.status_code == 201:
        print("Role assigned successfully.")
    else:
        print(f"Failed: {resp.status_code} - {resp.text}")

def main():
    token = get_access_token()
    apps = load_app_role_mapping()

    for app in apps:
        print(f"Processing app: {app['name']}")
        service_principal_id = app["service_principal_id"]

        for assignment in app["role_assignments"]:
            # your line goes here
            assign_app_role_to_group(
        token,
        assignment["group_id"],
        service_principal_id,
        assignment["app_role_id"],
    )

if __name__ == "__main__":
       main()