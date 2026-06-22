import os
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

GROUP_ID = "2b58b8ed-3e21-4e22-b2ff-4ce3637ea057"
SERVICE_PRINCIPAL_ID = "9f80de3f-8ea9-4a61-9359-8cf03b69dcdb"
APP_ROLE_ID = "afcdbfa7-9d27-4d79-beb9-af30ddabb013"  # Admin role — swap for Viewer to test the other one

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

if __name__ == "__main__":
    token = get_access_token()
    assign_app_role_to_group(token, GROUP_ID, SERVICE_PRINCIPAL_ID, APP_ROLE_ID)
