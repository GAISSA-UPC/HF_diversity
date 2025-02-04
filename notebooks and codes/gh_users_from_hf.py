""" Using both the HF and GitHub APIs to get GitHub information from the Hugging Face profile. """

import requests
from bs4 import BeautifulSoup
import pandas as pd

GITHUB_TOKEN = ""

def get_github_from_huggingface(username):
    hf_profile_url = f"https://huggingface.co/{username}"
    response = requests.get(hf_profile_url)
    
    if response.status_code != 200:
        print(f"Could not retrieve Hugging Face profile for {username}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for the GitHub profile link in the Hugging Face page
    github_section = None
    for link in soup.find_all('a', href=True):
        if "github.com" in link['href']:  # Check if the href contains a GitHub link
            github_section = link
            break
    
    if github_section:
        return github_section['href']
    else:
        print(f"No GitHub profile found for {username}")
        return None

def get_location_from_github(github_profile_url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}" 
    }

    response = requests.get(github_profile_url, headers=headers)  # Pass the headers with token
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for the location section in GitHub profile
    location_section = soup.find(itemprop='homeLocation')  # Use 'homeLocation' for location info
    
    if location_section:
        return location_section.get_text(strip=True)
    else:
        return None

def fetch_github_info_for_csv(csv_filename):
    df = pd.read_csv(csv_filename)
    
    if 'username' not in df.columns:
        print("CSV file must contain a 'username' column.")
        return
    
    df['has_github'] = False
    df['location'] = None
    
    for index, row in df.iterrows():
        hf_username = row['username']
        github_url = get_github_from_huggingface(hf_username)
        
        if github_url:
            df.at[index, 'has_github'] = True
            location = get_location_from_github(github_url)
            if location:
                df.at[index, 'location'] = location
        else:
            df.at[index, 'has_github'] = False
    
    updated_csv_filename = f"updated_{csv_filename}"
    df.to_csv(updated_csv_filename, index=False)

csv_filename = "google.csv" 
fetch_github_info_for_csv(csv_filename)


# cohen's kappa (> 0.80)

