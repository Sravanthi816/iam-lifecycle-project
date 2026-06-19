import os
import yaml
import msal
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -----------------------------
# Read configuration from YAML
# -----------------------------
with open("access-model.yaml", "r") as f:
    config = yaml.safe_load(f)

print("Groups loaded from access-model.yaml:")
for group in config["groups"]:
    print(f" - {group['name']}")

# -----------------------------
# Microsoft Graph Authentication
# -----------------------------
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

result = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" not in result:
    print("Failed to authenticate with Microsoft Graph API.")
    print(result.get("error"))
    print(result.get("error_description"))
    exit()

print("Successfully authenticated with Microsoft Graph API.")

headers = {
    "Authorization": f"Bearer {result['access_token']}",
    "Content-Type": "application/json"
}

# -----------------------------
# Create Groups
# -----------------------------
for group in config["groups"]:

    print(f"\nWorking on: {group['name']}")

    # Check if group already exists
    check_url = (
        "https://graph.microsoft.com/v1.0/groups"
        f"?$filter=displayName eq '{group['name']}'"
    )

    check_response = requests.get(
        check_url,
        headers=headers
    )

    check_response.raise_for_status()

    existing_groups = check_response.json().get("value", [])

    if existing_groups:
        print(
            f"Group already exists. "
            f"ID: {existing_groups[0]['id']}"
        )
        continue

    # Create group
    body = {
        "displayName": group["name"],
        "description": group["description"],
        "mailEnabled": False,
        "mailNickname": group["name"].replace("-", ""),
        "securityEnabled": True
    }

    create_response = requests.post(
        "https://graph.microsoft.com/v1.0/groups",
        headers=headers,
        json=body
    )

    if create_response.status_code == 201:
        created_group = create_response.json()

        print(
            f"Group created successfully. "
            f"ID: {created_group['id']}"
        )

    else:
        print(
            f"Failed to create group. "
            f"Status: {create_response.status_code}"
        )
        print(create_response.text)