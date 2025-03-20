# CSES CLI

![GitHub Actions](https://github.com/csesfi/cses-cli/actions/workflows/main.yml/badge.svg)
![Test server](https://github.com/csesfi/cses-cli/actions/workflows/server.yml/badge.svg)
[![codecov](https://codecov.io/gh/csesfi/cses-cli/branch/main/graph/badge.svg)](https://app.codecov.io/gh/csesfi/cses-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

University of Helsinki, Ohjelmistotuotantoprojekti (Software Engineering Project), summer 2021

CSES CLI is a lightweight tool for using CSES from the command line.

[CSES](https://cses.fi/) is an online platform for programming courses and contests. The platform is used in University of Helsinki courses *Data Structures and Algorithms* and *Algorithms for Solving Problems*.

## Application

- [Releases](https://github.com/csesfi/cses-cli/releases)

## Documentation

### User guides

- [Installation](https://github.com/csesfi/cses-cli/wiki/Installation)

- [User manual](https://github.com/csesfi/cses-cli/wiki/User-manual)

### Project managment

- [Google Drive folder](https://drive.google.com/drive/folders/1teZTWPnbmWlJkVfETz7T2j04UHqJYpuf?usp=sharing)

- [Backlogs + work time monitoring](https://docs.google.com/spreadsheets/d/10vB2CXV9RVyM_wIMyXrgepMcKMDzQ1qXHvmtuqjiaio/edit#gid=0)

- [Definition of Done and project guidelines](https://docs.google.com/document/d/1HzQkxhqxwODUW_URyV2goGciKnT3nIeE2NJFh6VS_qg/edit?usp=sharing)

### Program description

- [API](https://csesfi.github.io/cses-cli/)

- [Architecture](https://github.com/csesfi/cses-cli/wiki/Architecture)

- [Testing](https://github.com/csesfi/cses-cli/wiki/Testing)

## Tests downloader script

# 📥 CSES Test Case Downloader

This script downloads test cases from the **CSES problem set** and extracts them into a specified directory.

---

## 🛠️ **Setup Instructions**

### 1️⃣ Install Python (If Not Installed)
Ensure you have **Python 3** installed. Check by running:
```sh
python3 --version
```
If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

---

### 2️⃣ Create and Activate a Virtual Environment
To avoid dependency issues, it's **recommended** to run the script inside a Python virtual environment.

#### **For Linux/macOS:**
```sh
python3 -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate the environment
```

#### **For Windows (PowerShell):**
```powershell
python -m venv venv  # Create virtual environment
venv\Scripts\activate  # Activate the environment
```

Once activated, your terminal should **show `(venv)`** at the beginning of the prompt.

---

### 3️⃣ Install Required Dependencies
After activating the virtual environment, install the required packages:
```sh
pip install bs4 requests
```

---

### 4️⃣ Make the Script Executable (Linux/macOS)
If you're on **Linux or macOS**, make the script executable:
```sh
chmod +x downloader.py
```
This allows you to run it as:
```sh
./downloader.py -t 1234 -f my_tests -u my_user -p my_pass
```

---

## 🚀 **Usage**
After setting up the environment, you can run the script using:

```sh
python downloader.py -t <task_number> -f <directory_name> -u <username> -p <password>
```

### **Example:**
```sh
python downloader.py -t 1234 -f my_tests -u my_user -p my_pass
```
- The script will ask for a **root directory** on the first run and save it.
- Future runs will use the **saved root directory** automatically.

---

### **Override Root Directory (Optional)**
If you need to **change the root directory**, use the `-r` flag:
```sh
python downloader.py -t 1234 -r /home/user/cses_tests -f my_tests -u my_user -p my_pass
```
This will update the **root directory in `config.json`**.

---

## 📜 **Help Command**
To see all available options, run:
```sh
python downloader.py --help
```


## Contributors

The original version of this program was created during the *Software Engineering Project* course  (Ohjelmistotuotantoprojekti) at the University of Helsinki summer 2021.

### CSES-CLI software engineering project team  
- Antto Heikura
- Joona Huuhtanen
- Kalle Luopajärvi
- Roope Salmi
- Anton Taleiko
