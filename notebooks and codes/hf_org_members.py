""" Using the HF API to fetch information about the members of the studied organizations. """

import requests
import csv


def get_org_members(org_name):
    api_url = f"https://huggingface.co/api/organizations/{org_name}/members"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Could not retrieve organization members for {org_name}. Status Code: {response.status_code}")
        return []

    members_data = response.json()

    members = []
    
    for member in members_data:
        username = member.get("user", "")
        name = member.get("fullname", "")
        role = member.get("type", "")
        members.append((username, name, role))
    
    return members

def save_members_to_csv(org_name, members):
    csv_filename = f"{org_name}.csv"
    
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "name", "role"])
        writer.writerows(members)
    
    print(f"Saved {len(members)} members to {csv_filename}")

org_name = "google"
members = get_org_members(org_name)

if members:
    save_members_to_csv(org_name, members)
