import bcrypt
hash_val = b'/Rwx1gcVtm.hMiVFvQUxeDQtJLaNbQFgpMQRERYK2CpvMRZvyG5a'
for p in ['admin', 'admin123', 'admin', 'password', '1234', '123456', '123']:
    try:
        if bcrypt.checkpw(p.encode(), hash_val):
            print(f'Found: {p}')
    except: pass
