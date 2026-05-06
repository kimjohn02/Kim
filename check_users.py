import mysql.connector
import bcrypt

conn = mysql.connector.connect(host='localhost', user='root', password='', database='pos_system', use_pure=True)
cursor = conn.cursor()
cursor.execute('SELECT username, password, role, active FROM users')
rows = cursor.fetchall()
conn.close()

print('=== ALL USERS ===')
for row in rows:
    username, hashed, role, active = row
    is_bcrypt = hashed.startswith('$2b$') or hashed.startswith('$2a$')
    if is_bcrypt:
        print(f'User: {username} | Role: {role} | Active: {active} | Password: [bcrypt hashed]')
    else:
        print(f'User: {username} | Role: {role} | Active: {active} | Password (plain): {hashed}')
