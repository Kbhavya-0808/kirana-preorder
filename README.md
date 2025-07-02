# kirana-preorder
A simple Flask &amp; SQLite–based Kirana Pre‑Order Website Let your customers submit grocery orders (no login), check their status, and let the shop owner manage, pack, and even delete orders via a protected admin panel. Built with Bootstrap‑style custom CSS for a clean, responsive UI.
# Kirana Pre‑Order

A lightweight web app for small grocery (kirana) shops to accept pre‑orders and manage packing—all without the usual checkout queue.

## 🔑 Features

- **Customer Interface**  
  - Submit an order by entering just name, phone, and item list  
  - Check order status (Pending / Packed) or delete their order

- **Owner/Admin Dashboard**  
  - Secure login (`admin` / `admin123`)  
  - View, update status, set total amount, and delete orders  
  - Export orders to Excel (optional extension)

- **Tech Stack**  
  - Backend: Python & Flask  
  - Database: SQLite (`database.db`)  
  - Frontend: HTML5, CSS3 (custom responsive styling)  
  - Optional: dotenv for secure credentials, Twilio/SMS integratins 
