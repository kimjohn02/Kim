import mysql.connector
import bcrypt

# New password to set
new_password = "admin123"
username = "admin"

# Hash the new password
hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Update in database
conn = mysql.connector.connect(host='localhost', user='root', password='', database='pos_system', use_pure=True)
cursor = conn.cursor()
cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed, username))
conn.commit()
conn.close()

print(f"Password for '{username}' has been reset to: {new_password}")
print("You can now login with:")
print(f"  Username: {username}")
print(f"  Password: {new_password}")
