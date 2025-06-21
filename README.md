# Gmail Inbox Manager

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-yellow)
![Google OAuth2](https://img.shields.io/badge/OAuth2-Google-red)
![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue)

## 📄 Project Overview

Gmail Inbox Manager is a web-based application built with **Flask** and integrated with the **Gmail API** to offer a seamless experience for Gmail users to:

* Sign in via Google OAuth2
* View and categorize their emails
* Send new emails
* Delete selected messages
* Filter messages by category or month

## 🔧 Features

* **OAuth2 Authentication** for secure Google account access
* **Inbox Fetching** with custom classification:

  * EDUCATIONAL
  * SOCIAL
  * E-COMMERCE
  * PAYMENTS
  * VERIFICATION CODE
  * COMMUNITY
  * PRIMARY
* **Email Composition** through Gmail API
* **Email Deletion** with multi-select capability
* **Sorting by Month** or Category
* **Responsive UI** with Bootstrap styling

## 📁 Project Structure

```
├── quickstart.py          # Main Flask app
├── templates/
│   ├── index.html         # Google login page
│   ├── inbox.html         # Email dashboard with filters and actions
│   └── compose.html       # Email composition form
├── static/
│   ├── credentials.json   # OAuth2 credentials from Google Developer Console
│   └── token.json         # Saved access token after login
```

## 📊 Setup Instructions

### Prerequisites:

* Python 3.10+
* Flask
* Google API Client Libraries

### Install Dependencies

```bash
pip install flask google-auth google-auth-oauthlib google-api-python-client
```

### Google API Setup:

1. Go to the [Google Developer Console](https://console.developers.google.com/)
2. Enable Gmail API
3. Create OAuth 2.0 Client ID (type: Desktop or Web)
4. Download the `credentials.json` and place it in the `static/` folder

### Run Application

```bash
python quickstart.py
```

Access it at `http://127.0.0.1:5000`

## 🔎 Screenshots

### Login Page

![Login](https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg)

### Inbox View with Filters

(Screenshot not included here)

### Compose Email

(Screenshot not included here)

## 🚀 Future Improvements

* Pagination support
* Real-time push notifications
* Better error handling and retry mechanism
* Integration with Google Contacts API

## 📄 License

This project is licensed under the **GNU GPL v3**.

---

Made with ❤️ using Flask and Gmail API.
