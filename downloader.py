import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os
import sys
import argparse
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

def save_config(root_directory, username, password):
    """Saves login data and root directory to a configuration file."""
    config = {"root_directory": root_directory, "username": username, "password": password}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print(f"Configuration saved to {CONFIG_FILE}")

def load_config():
    """Loads login data and root directory from the configuration file if it exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def get_credentials(cli_username, cli_password):
    """Retrieves login credentials, either from CLI or stored config."""
    config = load_config()
    
    username = cli_username or config.get("username")
    password = cli_password or config.get("password")
    
    if not username or not password:
        username = input("Enter your CSES username: ").strip()
        password = input("Enter your CSES password: ").strip()
        save_config(config.get("root_directory"), username, password)
    
    return username, password

def get_root_directory(cli_root_directory):
    """Retrieves the root directory, either from CLI or stored config."""
    config = load_config()
    root_directory = cli_root_directory or config.get("root_directory")
    
    if not root_directory:
        root_directory = input("Enter the root directory to store test cases: ").strip()
        save_config(root_directory, config.get("username"), config.get("password"))
    
    return root_directory

def extract_csrf_token(html):
    """Extracts CSRF token from an HTML page."""
    soup = BeautifulSoup(html, 'html.parser')
    csrf_token_input = soup.find('input', {'name': 'csrf_token'})
    return csrf_token_input['value'] if csrf_token_input else None

def login(session, username, password):
    """Logs into CSES and returns a session with authentication."""
    login_url = "https://cses.fi/login"
    response = session.get(login_url)
    csrf_token = extract_csrf_token(response.text)
    
    if not csrf_token:
        print("CSRF token not found.")
        return False

    login_data = {"csrf_token": csrf_token, "nick": username, "pass": password}
    headers = {"Referer": login_url, "User-Agent": "Mozilla/5.0"}
    response = session.post(login_url, data=login_data, headers=headers)
    
    if "Logout" in response.text or "/logout" in response.text:
        print("Login successful!")
        return True
    else:
        print("Login failed.")
        return False

def download_zip(session, task_number):
    """Downloads the test case ZIP file and returns its content."""
    url = f"https://cses.fi/problemset/tests/{task_number}/"
    response = session.get(url)
    
    if "Login" in response.text:
        print("Access denied. You need to log in first.")
        return None
    
    csrf_token = extract_csrf_token(response.text)
    if not csrf_token:
        return None

    download_data = {"csrf_token": csrf_token, "download": "true"}
    headers = {"Referer": url, "User-Agent": "Mozilla/5.0"}
    download_response = session.post(url, data=download_data, headers=headers)
    
    if download_response.status_code != 200 or 'Content-Disposition' not in download_response.headers:
        print("Failed to download the ZIP file.")
        return None
    
    print("Download complete!")
    return download_response.content

def extract_zip(zip_content, root_directory, directory_name):
    """Extracts ZIP content into the specified directory inside the root directory."""
    extract_dir = os.path.join(root_directory, directory_name, "tests")
    os.makedirs(extract_dir, exist_ok=True)
    
    with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
        zip_file.extractall(extract_dir)
    
    print(f"Extraction complete! Files saved in {extract_dir}")

def run(task_number, root_directory, directory_name, username, password):
    """Runs the download and extraction process."""
    session = requests.Session()
    if not login(session, username, password):
        return
    zip_content = download_zip(session, task_number)
    if zip_content:
        extract_zip(zip_content, root_directory, directory_name)

help_text = """
CSES Test Case Downloader

This script downloads test cases from the CSES problem set and extracts them into a specified directory.

USAGE:
    python downloader.py -t <task_number> -f <directory_name> -u <username> -p <password>

OPTIONS:
    -t, --task_number      The CSES problem task number (required).
    -f, --directory_name   Task's subdirectory name e.g. hanoi (required).
    -u, --username         Your CSES username (required).
    -p, --password         Your CSES password (required).
    -r, --root_directory   (Optional) Set the root CSES directory for downloads. If not set, the script will ask once and save it.

EXAMPLES:
    First time setup (asks for root directory):
        python downloader.py -t 1234 -f my_tests -u my_user -p my_pass
    
    Automatically uses saved root directory:
        python downloader.py -t 5678 -f another_test -u my_user -p my_pass
    
    Override the root directory:
        python downloader.py -t 91011 -r /tmp/cses_tests -f my_tests -u my_user -p my_pass

NOTES:
    - The script saves the root directory in a config.json file in the same directory as the script.
    - If -r is provided, the root directory is updated in config.json.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-t", "--task_number", help="The CSES task number", required=False)
    parser.add_argument("-f", "--directory_name", help="Task's subdirectory name e.g. hanoi", required=False)
    parser.add_argument("-u", "--username", help="Your CSES username")
    parser.add_argument("-p", "--password", help="Your CSES password")
    parser.add_argument("-r", "--root_directory", help="CSES root directory")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    
    args = parser.parse_args()
    
    if args.help or len(sys.argv) == 1:
        print(help_text)
        sys.exit(0)
    
    root_directory = get_root_directory(args.root_directory)
    username, password = get_credentials(args.username, args.password)
    run(args.task_number, root_directory, args.directory_name, username, password)