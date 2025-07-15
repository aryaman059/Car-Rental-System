# 🚗 Car Rental System - Python + Tkinter + MySQL

A **GUI-based Car Rental System** application built using **Python**, **Tkinter**, and **MySQL** to simulate a real-time car booking service. This system allows users to rent cars, view available vehicles, and store all interactions in a relational database.

## 💡 Features

- 🧑‍💼 Add and manage customers and employees
- 🚙 Add, update, and view available vehicles
- 📅 Book/reserve cars with user details and rental period
- 💾 Integrated with MySQL to store:
  - Customer data
  - Employee data
  - Vehicle inventory
  - Reservation records
  - Rental history
- ✅ Easy-to-use and beginner-friendly GUI
- 📉 Real-time vehicle availability management

## 🛠️ Tech Stack

- **Language:** Python 3.x  
- **GUI Library:** Tkinter  
- **Database:** MySQL (via `mysql-connector-python`)  
- **IDE Recommended:** VS Code / PyCharm  

## 🗃️ Database Schema Overview

- `Customer(id, name, phone, email, license_no)`
- `Employee(id, name, position)`
- `Vehicle(id, model, type, availability)`
- `Reservation(id, customer_id, vehicle_id, start_date, end_date)`
- `Rent(id, reservation_id, total_cost, status)`

All foreign key relationships and data validations are maintained in the schema.

## 🔧 How It Works

1. Customer info is entered or selected.
2. Vehicle availability is fetched live from the database.
3. Reservation and rental records are created.
4. Vehicle status is updated (available/unavailable).
5. All interactions are stored in MySQL for easy tracking and reporting.

