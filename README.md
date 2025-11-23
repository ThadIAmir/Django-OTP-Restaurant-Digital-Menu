<div align="center">

# 🌙 Django-OTP-Restaurant-Digital-Menu  
Modern Glassmorphism Digital Menu System with Secure OTP Login

---

## 🔰 Badges

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-darkgreen?logo=django)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)
![Made With Love](https://img.shields.io/badge/Made%20With-Love-red)

---

## 🖼️ Tech Logos

<p align="center">
  <!-- <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/python.svg" width="80" /> -->
  <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/django.svg" width="80" />
  <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/postgresql.svg" width="80" />
  <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/javascript.svg" width="80" />
</p>

</div>

---

# 🚀 Project Overview

A full-stack, responsive digital menu system built with **Django** and a modern **Royal Night (Glassmorphism)** UI.  
This project highlights backend engineering: secure authentication, state persistence, real-time AJAX, and clean database structure.

---

# 🌟 Key Features of This Project

### 🔐 OTP Authentication (API + Fallback)

- Two-step login using **One-Time Passwords (OTP)**.
- Integrated external SMS provider (e.g., **Kavenegar**) via `KAVENEGAR_API_KEY`.
- **Automatic fallback:** if the SMS API fails or the API key is invalid → OTP is printed directly to the server console.
- OTP codes expire in **120 seconds**, fully enforced in backend logic.

---

### 🛒 Persistent Cart Logic

- Anonymous users → stored using **Django Sessions**
- Authenticated users → stored using the **CartItem model**
- On login → the session cart **automatically merges** into the user’s database cart, ensuring nothing is lost.

---

### ⚡ AJAX APIs (Real-Time Cart Updates)

- Built JSON endpoints for instant cart interactions:
  - `add_to_basket_api`
  - `update_basket_api`
- Updates **totals**, **discounts**, and **quantities** without any page reload.

---

### 🗄 Clean Database Architecture

- Clear separation between:
  - **Mutable data** → live cart items
  - **Immutable data** → order history (ready for checkout implementation)
- Designed for scalability and long-term maintenance.


---

## 🛠️ Tech Stack

| Category | Technology |
|---------|------------|
| Backend | Django 4.2.x |
| Language | Python 3.12+ |
| Database | PostgresQL |
| Authentication | Sessions + Custom OTP |
| Frontend | AJAX, Vanilla JS, Django Templates |
| Security | python-decouple |

---

# ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thadiamir/Django-OTP-Restaurant-Digital-Menu.git
cd Django-OTP-Restaurant-Digital-Menu
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` . Update details as needed.

### 5. Run migrations
```bash
python manage.py migrate

# also create the superuser for later admin panel usages
python manage.py createsuperuser
```

### 6. Start the application
```bash
python manage.py runserver
```



### 7. Access the Application

Open your browser and go to: `http://127.0.0.1:8000`

---

# 🔑 How to Test the OTP System

Since this project is configured for **Console Fallback** by default, you can fully test the secure authentication flow without needing to pay for or register with a real SMS provider.

1.  Navigate to the Login page (`/login`).
2.  Enter any 11-digit Iranian mobile format number (e.g., `09123456789`).
3.  **Check your terminal/console** where `python manage.py runserver` is running. The 4-digit OTP will be printed there (e.g., `ROYAL TEHRAN OTP: 4823`).
4.  Enter the code in the browser to log in.

### ⏳ Testing Expiry

* Try waiting **125 seconds** (2 minutes + buffer) before entering the code. The backend logic will reject the code, demonstrating the server-side security measure.

---

# 🤝 Contribution & Licensing

Contributions, issues, and feature requests are welcome! Feel free to check the [Issues Page](https://github.com/thadiamir/Django-OTP-Restaurant-Digital-Menu/issues) if you find any bugs or have ideas for enhancements.

This project is licensed under the **MIT License**.

---

# 👤 Author & Contact

This project was built by **ME**, focusing on backend development, data persistence, and secure authentication.

* **GitHub:** [@ThadIAmir](https://github.com/Thadiamir)
* **LinkedIn:** [@Amir-Hosseini](www.linkedin.com/in/amir-hosseini-699a55245)

***
*© 2025 Amir Hosseini. All Rights Reserved.*
