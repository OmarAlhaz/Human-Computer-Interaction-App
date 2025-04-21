# 🧠 Human-Computer Interaction App

An interactive desktop app built with **Python** and **Firebase**, enabling users to manage reminders, send SMS messages, schedule appointments, and visualize weather/location data—all through a user-friendly GUI.

---

## 🚀 Features

- 📅 Create and manage reminders and appointments  
- 📲 Send SMS and view contact/device data  
- 📍 Visualize location using custom maps  
- 🌦️ Check weather and receive Firebase-based alerts  
- 🔐 Secure cloud-based data sync with Firebase  
- 🖥️ GUI with custom Tkinter and advanced widgets  

---

## 🧰 Tech Stack

| Layer       | Technology            |
|------------|------------------------|
| UI         | Python, `customtkinter` |
| Cloud Sync | Firebase Realtime DB   |
| Backend    | Python, `firebase_admin`, `requests`, `PIL`, `datetime`, `tkintermapview` |
| Email      | `smtplib`, Gmail SMTP  |

---

## 🖼️ App Screenshots

| Home Panel | Weather Forecast | Wiki Search | Map Panel |
|------------|------------------|-------------|-----------|
| ![home](./App_screenshots/Home.png) | ![weather](./App_screenshots/Weather.png) | ![wiki](./App_screenshots/Search.png) | ![map](./App_screenshots/Map.png) |


---

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/OmarAlhaz/Human-Computer-Interaction-App.git
cd hci-firebase-app
```

### 2️⃣ Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install the required libraries

```bash
pip install -r requirements.txt
```

> Or manually:

```bash
pip install firebase-admin requests pillow customtkinter tkintermapview
```

### 4️⃣ Setup environment variables

Copy `.env.example` and fill in credentials:

```bash
cp .env.example .env
```

---

## 🛠️ Running the App

```bash
python main.py
```

> If you're on Windows and encounter permission issues:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 🧪 Libraries Used

- `firebase-admin`: Firebase authentication & database  
- `requests`: API calls & online data fetch  
- `tkinter` + `customtkinter`: Graphical user interface  
- `PIL`: Image processing  
- `datetime`: Scheduling logic  
- `tkintermapview`: Map visualizations  
- `smtplib`: Email messaging (Gmail)  

---

## 🔐 Credentials

You must create a Firebase service account and add your project credentials in the `.env` file.

Firebase Setup → [https://console.firebase.google.com](https://console.firebase.google.com)  
Generate App Password (for Gmail) → [Google Account Security](https://myaccount.google.com/security)

---

## 📂 Folder Structure

```bash
📦 hci-firebase-app/
 ┣ 📂App_screenshots/
 ┣ 📄main.py
 ┣ 📄requirements.txt
 ┣ 📄.env.example
 ┣ 📄.gitignore
 ┣ 📄README.md
```

---

## 🙌 Acknowledgements

Developed as part of a Human-Computer Interaction academic project. All Firebase services are secured and user interactions are locally stored or synced with the cloud.
