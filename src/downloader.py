import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os
import sys

def login(session, username, password):
    """Logs into CSES and returns a session with authentication."""
    login_url = "https://cses.fi/login"
    
    # Get the login page to retrieve the CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract CSRF token
    csrf_token_input = soup.find('input', {'name': 'csrf_token'})
    if not csrf_token_input:
        print("Failed to retrieve CSRF token for login.")
        return False

    csrf_token = csrf_token_input['value']
    
    login_data = {
        "csrf_token": csrf_token,
        "nick": username,
        "pass": password
    }

    headers = {
        "Referer": login_url,
        "User-Agent": "Mozilla/5.0"
    }

    # Send the login request
    response = session.post(login_url, data=login_data, headers=headers)

    # Debugging: Check if login was successful
    if "Logout" in response.text or "/logout" in response.text:
        print("Login successful!")
        return True
    else:
        print("Login failed. Debugging response:")
        print(response.text[:1000])  # Print first 1000 characters of response
        return False

def download_and_extract(session, task_number):
    """Downloads and extracts the test case ZIP file."""
    base_url = "https://cses.fi/problemset/tests/"
    url = f"{base_url}{task_number}/"

    response = session.get(url)
    
    # Debugging: Print fetched HTML
    print("Fetched HTML Content:")
    print(response.text[:1000])

    if "Login" in response.text:
        print("Access denied. You need to log in first.")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})

    if not csrf_token:
        print("CSRF token not found. Cannot proceed with download.")
        return

    csrf_token_value = csrf_token['value']
    download_data = {
        "csrf_token": csrf_token_value,
        "download": "true"
    }

    headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0"
    }

    download_response = session.post(url, data=download_data, headers=headers)

    if download_response.status_code != 200 or 'Content-Disposition' not in download_response.headers:
        print("Failed to download the ZIP file.")
        return

    # Extract the ZIP file
    zip_file = zipfile.ZipFile(io.BytesIO(download_response.content))
    zip_file.extractall(os.getcwd())
    print("Download and extraction complete!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <task_number> <username> <password>")
        sys.exit(1)
    
    task_number = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    session = requests.Session()
    
    if login(session, username, password):
        download_and_extract(session, task_number)
