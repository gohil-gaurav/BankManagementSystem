# 🏦 Bank Management System

A **Django-based Bank Management System** that simulates core banking operations such as account management, transactions, approvals, and role-based access control.

This project is built for **learning, portfolio demonstration, and real-world workflow simulation**.  
It is **not intended for real banking use**.

---

## 🚀 Project Overview

The **Bank Management System** is a full-stack web application that allows:

- **Customers** to manage bank accounts and perform transactions  
- **Managers** to supervise accounts, approve transactions, and generate reports  
- **Admins** to control the system using Django Admin  

The project focuses on **backend logic, database relationships, authentication, authorization, and deployment** using Django.

---

## 👥 User Roles

### 🔑 Admin
- Full access to Django Admin panel
- Manage all users, accounts, and transactions
- Monitor system-wide activity
- Perform administrative actions

### 🧑‍💼 Manager
- Access manager dashboard
- View users and accounts
- Freeze / unfreeze accounts
- Approve or reject transactions
- Generate and view reports
- Monitor system activity

### 👤 Customer (Bank User)
- Register and log in
- View personal dashboard
- Deposit and withdraw money
- View transaction history
- Check account balance and status

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- User registration and login
- Role-based access control
- Secure password handling using Django Auth
- Protected routes and permissions

### 💳 Account Management
- Automatic account creation
- Unique account numbers
- Balance tracking
- Account freeze/unfreeze functionality

### 💰 Transaction Management
- Deposit and withdrawal operations
- Balance validation
- Transaction status tracking
- Complete transaction history

### ✅ Approval System
- Manager approval for transactions
- Pending transaction queue
- Approval and rejection workflow
- Action logging

### 📊 Dashboards & Reports
- Role-based dashboards
- Transaction summaries
- User and account monitoring
- System statistics

### 📱 Responsive UI
- Mobile-friendly design
- Hamburger menu for mobile view
- Clean and simple interface

---

## 🛠 Tech Stack

### Backend
- Python
- Django
- Django ORM
- Django Authentication System

### Frontend
- HTML (Django Templates)
- CSS
- JavaScript (basic)

### Database
- SQLite (for development and demo)

### Deployment
- PythonAnywhere

### Version Control
- Git & GitHub

---

## 🗂 Project Structure
```
BankManagementSystem/
├── manage.py
├── requirements.txt
├── config/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── apps/
│ ├── users/ # Authentication & user management
│ └── bank/ # Banking logic & dashboards
│
├── templates/
│ ├── base.html
│ ├── users/
│ └── bank/
│
├── static/
│ ├── css/
│ └── js/
│
└── db.sqlite3
```
---

## 🧠 Backend Architecture

- Django MVT (Model–View–Template) architecture
- Separate apps for authentication and banking logic
- Role-based permission checks
- Django signals for automatic account creation
- Custom dashboards and views

---

## 🗄 Database Design (High Level)

Main models include:
- User (Django built-in)
- Account
- Transaction
- ManagerAction

Relationships:
- One User → One Account
- One Account → Many Transactions
- One Manager → Many Actions

---

## 🔒 Security Features

- Password hashing
- CSRF protection
- Form validation
- Role-based access restrictions
- ORM-based queries (SQL injection safe)

---

## ⚠️ Limitations

- Not a real banking system
- Uses SQLite (not production scalable)
- No payment gateway integration
- No OTP or email verification
- No advanced fraud detection

---

## 🚧 Future Enhancements

- PostgreSQL / MySQL integration
- Email and notification system
- PDF / CSV report export
- Loan management module
- REST API support
- Docker-based deployment

---

## 🎤 Interview Explanation

**Short explanation:**

> “This is a Django-based Bank Management System with role-based access for admins, managers, and customers. It supports account management, transactions, approvals, dashboards, and reports, and is deployed on PythonAnywhere.”

---

## 📌 Summary

This project demonstrates:
- Strong Django fundamentals
- Backend logic and database design
- Authentication and authorization
- Clean UI with responsive design
- Real deployment experience

---

## 📎 Disclaimer

This project is for **educational and portfolio purposes only** and does **not represent a real banking system**.
