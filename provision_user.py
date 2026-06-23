import os
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

# (department, title) -> groups
GROUP_RULES = {
    ("Engineering", "Manager"): [
        "2b58b8ed-3e21-4e22-b2ff-4ce3637ea057",  # SG-Engineering-Admins
        "25c56245-3a9a-4077-8bca-6ecc289b69f2",  # SG-Engineering-Vancouver
    ],

    ("Engineering", "Senior Lead"): [
        "2b58b8ed-3e21-4e22-b2ff-4ce3637ea057",
        "25c56245-3a9a-4077-8bca-6ecc289b69f2",
    ],

    ("Engineering", "Junior"): [
        "25c56245-3a9a-4077-8bca-6ecc289b69f2",
    ],

    ("Finance", "Manager"): [
        "10d0f57b-d720-40d1-93b7-e8ef1bdea92d",  # SG-Finance-Admins
        "fb37b0cb-35b8-4c90-85c4-360221ded16a",  # SG-Finance-Vancouver
    ],

    ("Finance", "Junior"): [
        "fb37b0cb-35b8-4c90-85c4-360221ded16a",
    ],
}


def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET,
    )

    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in result:
        raise Exception(
            f"Failed to get token: {result.get('error_description')}"
        )

    return result["access_token"]


def add_user_to_group(token, user_id, group_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = (
        f"https://graph.microsoft.com/v1.0/"
        f"groups/{group_id}/members/$ref"
    )

    body = {
        "@odata.id":
        f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
    )

    if response.status_code == 204:
        print(f"[SUCCESS] Added user to group {group_id}")

    elif response.status_code == 400:
        if "already exist" in response.text.lower():
            print(
                f"[INFO] User already member of group {group_id}"
            )
        else:
            print(
                f"[ERROR] {response.status_code} - {response.text}"
            )

    else:
        print(
            f"[ERROR] {response.status_code} - {response.text}"
        )


def provision_user(token, user_id, department, title):

    department = department.strip()
    title = title.strip()

    groups = GROUP_RULES.get((department, title))

    if not groups:
        print(
            f"[WARNING] No rule defined for "
            f"{department} / {title}"
        )
        return

    print(
        f"[MATCH] {department} / {title} "
        f"-> {len(groups)} group(s)"
    )

    for group_id in groups:
        add_user_to_group(
            token,
            user_id,
            group_id,
        )


if __name__ == "__main__":

    token = get_access_token()

    provision_user(
        token,
        "b637c006-0c15-41c7-a461-9c4e78acc186",
        "Engineering",
        "Manager",
    )