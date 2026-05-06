import datetime
import os

# --- MOCK DATABASE ---
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "cashier": {"password": "cashier123", "role": "cashier"}
}

# Pre-populated computer parts inventory
inventory = {
    "1": {"name": "Intel Core i7 CPU", "price": 320.0, "stock": 15},
    "2": {"name": "AMD Ryzen 5 CPU", "price": 200.0, "stock": 20},
    "3": {"name": "NVIDIA RTX 4060 GPU", "price": 400.0, "stock": 8},
    "4": {"name": "16GB Corsair DDR4 RAM", "price": 60.0, "stock": 30},
    "5": {"name": "1TB Samsung NVMe SSD", "price": 85.0, "stock": 25},
    "6": {"name": "ASUS B550 Motherboard", "price": 140.0, "stock": 12},
    "7": {"name": "EVGA 650W Power Supply", "price": 75.0, "stock": 18}
}

transactions = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title):
    print(f"\n{'='*50}")
    print(f"{title.center(50)}")
    print(f"{'='*50}")

# ---------------------------------------------------------
# 1. LOGIN MODULE
# ---------------------------------------------------------
def login_module():
    """Authenticates users and redirects based on role."""
    while True:
        display_header("LOGIN MODULE")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        
        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            print(f"\n✅ Login successful! Welcome, {username}.")
            return role
        else:
            print("\n❌ Invalid credentials. Please try again.")

# ---------------------------------------------------------
# 2. PRODUCT MANAGEMENT MODULE (INVENTORY)
# ---------------------------------------------------------
def product_management_module():
    """Admin module to Add, Update, Delete, or View products."""
    while True:
        display_header("PRODUCT MANAGEMENT (INVENTORY)")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Return to Admin Menu")
        
        choice = input("\nSelect an action (1-5): ")
        
        if choice == '1':
            p_id = input("Enter new Product ID: ")
            if p_id in inventory:
                print("❌ Product ID already exists!")
            else:
                name = input("Enter Product Name: ")
                try:
                    price = float(input("Enter Price: $"))
                    stock = int(input("Enter Stock Quantity: "))
                    inventory[p_id] = {"name": name, "price": price, "stock": stock}
                    print("✅ Product added successfully!")
                except ValueError:
                    print("❌ Invalid input for price or stock.")
                
        elif choice == '2':
            p_id = input("Enter Product ID to update: ")
            if p_id in inventory:
                name = input(f"Enter new Name ({inventory[p_id]['name']}): ") or inventory[p_id]['name']
                price_input = input(f"Enter new Price ({inventory[p_id]['price']}): ")
                stock_input = input(f"Enter new Stock ({inventory[p_id]['stock']}): ")
                
                inventory[p_id]['name'] = name
                if price_input:
                    try: inventory[p_id]['price'] = float(price_input)
                    except ValueError: print("❌ Invalid price. Keeping old value.")
                if stock_input:
                    try: inventory[p_id]['stock'] = int(stock_input)
                    except ValueError: print("❌ Invalid stock. Keeping old value.")
                    
                print("✅ Product updated successfully!")
            else:
                print("❌ Product not found.")
                
        elif choice == '3':
            p_id = input("Enter Product ID to delete: ")
            if p_id in inventory:
                confirm = input("Are you sure you want to delete this product? (y/n): ")
                if confirm.lower() == 'y':
                    del inventory[p_id]
                    print("✅ Product deleted successfully!")
            else:
                print("❌ Product not found.")
                
        elif choice == '4':
            print("\n--- Available Products ---")
            print(f"{'ID':<5} | {'Name':<25} | {'Price':<10} | {'Stock':<5}")
            print("-" * 55)
            for p_id, info in inventory.items():
                print(f"{p_id:<5} | {info['name']:<25} | ${info['price']:<9.2f} | {info['stock']:<5}")
                
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice. Please try again.")

# ---------------------------------------------------------
# 3. SALES MODULE
# ---------------------------------------------------------
def sales_module():
    """Cashier module to view products and add to cart."""
    cart = []
    while True:
        display_header("SALES MODULE")
        print("\n--- Available Products ---")
        print(f"{'ID':<5} | {'Name':<25} | {'Price':<10} | {'Stock':<5}")
        print("-" * 55)
        for p_id, info in inventory.items():
            print(f"{p_id:<5} | {info['name']:<25} | ${info['price']:<9.2f} | {info['stock']:<5}")
            
        print("\nOptions:")
        print("1. Add item to cart")
        print("2. Proceed to Cart/Checkout")
        print("3. Cancel & Logout")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == '1':
            p_id = input("Enter Product ID: ")
            if p_id in inventory:
                try:
                    qty = int(input("Enter desired quantity: "))
                    if qty > 0 and qty <= inventory[p_id]['stock']:
                        # Temporarily reduce stock to prevent overselling during this session
                        inventory[p_id]['stock'] -= qty
                        
                        # Check if item is already in cart
                        found = False
                        for item in cart:
                            if item['p_id'] == p_id:
                                item['qty'] += qty
                                item['subtotal'] = item['qty'] * inventory[p_id]['price']
                                found = True
                                break
                        
                        if not found:
                            cart.append({
                                'p_id': p_id,
                                'name': inventory[p_id]['name'],
                                'price': inventory[p_id]['price'],
                                'qty': qty,
                                'subtotal': qty * inventory[p_id]['price']
                            })
                        print("✅ Item added to cart.")
                    else:
                        print("❌ Invalid quantity or insufficient stock!")
                except ValueError:
                    print("❌ Please enter a valid number.")
            else:
                print("❌ Product not found.")
                
        elif choice == '2':
            if not cart:
                print("❌ Cart is empty! Please add items first.")
            else:
                # Proceed to next module
                cart_module(cart)
                break # After checkout completes, return to main menu (login)
                
        elif choice == '3':
            # Restore stock if cancelling
            for item in cart:
                inventory[item['p_id']]['stock'] += item['qty']
            print("Sale cancelled. Logging out...")
            break
        else:
            print("❌ Invalid choice.")

# ---------------------------------------------------------
# 4. CART MODULE
# ---------------------------------------------------------
def cart_module(cart):
    """Calculates subtotals and displays cart summary."""
    display_header("CART MODULE")
    print(f"{'Name':<25} | {'Qty':<5} | {'Price':<10} | {'Subtotal':<10}")
    print("-" * 60)
    
    total_amount = 0.0
    for item in cart:
        print(f"{item['name']:<25} | {item['qty']:<5} | ${item['price']:<9.2f} | ${item['subtotal']:<9.2f}")
        total_amount += item['subtotal']
        
    print("-" * 60)
    print(f"Total Amount: ${total_amount:.2f}")
    
    while True:
        proceed = input("\nProceed to payment? (y/n): ")
        if proceed.lower() == 'y':
            payment_module(cart, total_amount)
            break
        elif proceed.lower() == 'n':
            # Restore stock if cancelled
            for item in cart:
                inventory[item['p_id']]['stock'] += item['qty']
            print("Transaction cancelled. Returning to main menu.")
            break
        else:
            print("❌ Invalid choice. Enter 'y' or 'n'.")

# ---------------------------------------------------------
# 5. PAYMENT MODULE
# ---------------------------------------------------------
def payment_module(cart, total_amount):
    """Handles payment processing and change calculation."""
    display_header("PAYMENT MODULE")
    print(f"Total Amount Due: ${total_amount:.2f}")
    
    while True:
        try:
            payment = float(input("\nEnter customer's payment amount: $"))
            if payment >= total_amount:
                change = payment - total_amount
                print("✅ Payment sufficient!")
                receipt_module(cart, total_amount, payment, change)
                break
            else:
                print(f"❌ Insufficient payment! You need ${total_amount - payment:.2f} more.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

# ---------------------------------------------------------
# 6. RECEIPT MODULE
# ---------------------------------------------------------
def receipt_module(cart, total_amount, payment, change):
    """Generates and displays the transaction receipt."""
    display_header("RECEIPT MODULE")
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    receipt_text =  f"\n{'='*40}\n"
    receipt_text += f"        COMPUTER PARTS POS\n"
    receipt_text += f"        OFFICIAL RECEIPT\n"
    receipt_text += f"{'='*40}\n"
    receipt_text += f"Date/Time: {date_time}\n"
    receipt_text += f"{'-'*40}\n"
    
    for item in cart:
        receipt_text += f"{item['name'][:20]:<22} x{item['qty']:<3} ${item['subtotal']:>9.2f}\n"
        
    receipt_text += f"{'-'*40}\n"
    receipt_text += f"TOTAL:                     ${total_amount:>9.2f}\n"
    receipt_text += f"CASH:                      ${payment:>9.2f}\n"
    receipt_text += f"CHANGE:                    ${change:>9.2f}\n"
    receipt_text += f"{'='*40}\n"
    receipt_text += f"      Thank you for your purchase!\n"
    receipt_text += f"{'='*40}\n"
    
    print(receipt_text)
    
    # Save transaction record for Reports Module
    transactions.append({
        "datetime": date_time,
        "items": cart,
        "total": total_amount,
        "payment": payment,
        "change": change
    })
    
    input("Press Enter to complete and return to Main Menu...")

# ---------------------------------------------------------
# 7. REPORTS MODULE
# ---------------------------------------------------------
def reports_module():
    """Admin module to view sales, stock levels, and history."""
    while True:
        display_header("REPORTS MODULE")
        print("1. Daily Sales / Total Income")
        print("2. Low Stock Items")
        print("3. Transaction History")
        print("4. Return to Admin Menu")
        
        choice = input("\nSelect report type (1-4): ")
        
        if choice == '1':
            total_income = sum(t['total'] for t in transactions)
            print(f"\n--- Total Income ---")
            print(f"Total Sales Revenue: ${total_income:.2f}")
            print(f"Total Transactions: {len(transactions)}")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            print("\n--- Low Stock Items (Stock < 10) ---")
            found = False
            for p_id, info in inventory.items():
                if info['stock'] < 10:
                    print(f"[{p_id}] {info['name']} - Current Stock: {info['stock']}")
                    found = True
            if not found:
                print("✅ All items are well-stocked (10 or more).")
            input("\nPress Enter to continue...")
                
        elif choice == '3':
            print("\n--- Transaction History ---")
            if not transactions:
                print("No transactions recorded yet.")
            else:
                for i, t in enumerate(transactions, 1):
                    print(f"\nTransaction #{i} | {t['datetime']}")
                    print(f"Total: ${t['total']:.2f} | Payment: ${t['payment']:.2f} | Change: ${t['change']:.2f}")
                    for item in t['items']:
                        print(f"  - {item['name']} (x{item['qty']})")
            input("\nPress Enter to continue...")
                        
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice.")

# ---------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------
def main():
    while True:
        clear_screen()
        # Start at Login Module
        role = login_module()
        
        if role == "admin":
            while True:
                display_header("ADMIN MENU")
                print("1. Product Management (Inventory)")
                print("2. Reports")
                print("3. Logout")
                
                choice = input("\nSelect an option (1-3): ")
                if choice == '1':
                    product_management_module()
                elif choice == '2':
                    reports_module()
                elif choice == '3':
                    print("Logging out...")
                    break
                else:
                    print("❌ Invalid choice.")
                    
        elif role == "cashier":
            # Direct to Sales Module as per instructions
            sales_module()

if __name__ == "__main__":
    main()
