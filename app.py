
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'kirana_secret_key'
DATABASE = 'database.db'

# Initialize DB
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            items TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            total_amount TEXT DEFAULT '',
            timestamp TEXT
        )''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    items = request.form['items']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO orders (name, phone, items, timestamp) VALUES (?, ?, ?, ?)',
                     (name, phone, items, timestamp))
    return render_template('submitted.html')

@app.route('/check', methods=['GET', 'POST'])
def check_status():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.execute('SELECT items, status, total_amount FROM orders WHERE name=? AND phone=? ORDER BY id DESC LIMIT 1', (name, phone))
            row = cur.fetchone()
            if row:
                return render_template('status.html', items=row[0], status=row[1], amount=row[2])
            else:
                return render_template('status.html', not_found=True)
    return render_template('check.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = "❌ Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    with sqlite3.connect(DATABASE) as conn:
        orders = conn.execute('SELECT * FROM orders ORDER BY id DESC').fetchall()
    return render_template('admin.html', orders=orders)

@app.route('/admin/mark/<int:order_id>', methods=['POST'])
def mark_packed(order_id):
    status = request.form['status']
    amount = request.form['amount']
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('UPDATE orders SET status=?, total_amount=? WHERE id=?', (status, amount, order_id))
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/delete', methods=['GET', 'POST'])
def delete_order():
    deleted = None
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.execute('SELECT * FROM orders WHERE name=? AND phone=?', (name, phone))
            row = cur.fetchone()
            if row:
                conn.execute('DELETE FROM orders WHERE id=?', (row[0],))
                deleted = True
            else:
                deleted = False
    return render_template('delete.html', deleted=deleted)

@app.route('/admin/delete/<int:order_id>', methods=['POST'])
def delete_order_admin(order_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DELETE FROM orders WHERE id=?', (order_id,))
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
