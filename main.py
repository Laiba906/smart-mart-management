# Smart Mart Management System (Lab 12 Full Project)
# Author: Your Name
# Note: This is a simplified version that fulfills the lab requirements

import tkinter as tk
from tkinter import messagebox
import os

# --------------------- File Setup ---------------------
ADMIN_FILE = 'admin.txt'
PRODUCTS_FILE = 'products.txt'
CASHIERS_FILE = 'cashiers.txt'
BILLS_FILE = 'bills.txt'

# Ensure data files exist
for file in [ADMIN_FILE, PRODUCTS_FILE, CASHIERS_FILE, BILLS_FILE]:
    if not os.path.exists(file):
        open(file, 'w').close()

# --------------------- Utility Functions ---------------------
def read_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def write_file(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f"{line}\n")

def append_file(filename, line):
    with open(filename, 'a') as f:
        f.write(f"{line}\n")

#--------testing-------

def cashier_exists(username, filename=CASHIERS_FILE):
    cashiers = read_file(filename)
    for line in cashiers:
        if line.split(":")[0] == username:
            return True
    return False

def is_valid_login(username, password, filename):
    creds = read_file(filename)
    return f"{username}:{password}" in creds


# --------------------- Admin Panel ---------------------
class AdminPanel(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Admin Panel")
        self.geometry("400x400")
        tk.Label(self, text="Admin Controls", font=('Arial', 16)).pack(pady=10)

        # Frame for cashier management buttons and listbox
        frame = tk.Frame(self)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(side='top', fill='x')

        tk.Button(btn_frame, text="View Cashiers", command=self.view_cashiers).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Add Cashier", command=self.add_cashier).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Cashier", command=self.update_cashier).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Cashier", command=self.delete_cashier).pack(side='left', padx=5)

        self.cashier_listbox = tk.Listbox(frame)
        self.cashier_listbox.pack(fill='both', expand=True, pady=10)
        self.load_cashiers()

        tk.Button(self, text="Add Product Category", command=self.add_category).pack(fill='x')

    def load_cashiers(self):
        self.cashier_listbox.delete(0, 'end')
        data = read_file(CASHIERS_FILE)
        for line in data:
            self.cashier_listbox.insert('end', line)

    def view_cashiers(self):
        data = read_file(CASHIERS_FILE)
        messagebox.showinfo("Cashiers", "\n".join(data) or "No cashiers added yet.")

    def add_cashier(self):
        def save():
            uname = name.get().strip()
            pwd = password.get().strip()
            if not uname or not pwd:
                messagebox.showwarning("Warning", "Username and password cannot be empty.")
                return
            # Prevent duplicates
            existing = read_file(CASHIERS_FILE)
            for line in existing:
                if line.split(':')[0] == uname:
                    messagebox.showwarning("Warning", "Cashier username already exists.")
                    return
            append_file(CASHIERS_FILE, f"{uname}:{pwd}")
            messagebox.showinfo("Success", "Cashier added.")
            self.load_cashiers()
            popup.destroy()

        popup = tk.Toplevel(self)
        popup.title("Add Cashier")
        tk.Label(popup, text="Cashier Name").pack(pady=2)
        name = tk.Entry(popup)
        name.pack()
        tk.Label(popup, text="Password").pack(pady=2)
        password = tk.Entry(popup, show='*')
        password.pack()
        tk.Button(popup, text="Save", command=save).pack(pady=5)

    def update_cashier(self):
        selected = self.cashier_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a cashier to update.")
            return
        old_line = self.cashier_listbox.get(selected[0])
        old_uname, old_pwd = old_line.split(":")

        def save():
            new_uname = name.get().strip()
            new_pwd = password.get().strip()
            if not new_uname or not new_pwd:
                messagebox.showwarning("Warning", "Username and password cannot be empty.")
                return
            cashiers = read_file(CASHIERS_FILE)
            # Check if new username exists and is different from old username
            for line in cashiers:
                uname = line.split(":")[0]
                if uname == new_uname and new_uname != old_uname:
                    messagebox.showwarning("Warning", "Username already exists.")
                    return
            # Update the selected cashier
            cashiers[selected[0]] = f"{new_uname}:{new_pwd}"
            write_file(CASHIERS_FILE, cashiers)
            messagebox.showinfo("Success", "Cashier updated.")
            self.load_cashiers()
            popup.destroy()

        popup = tk.Toplevel(self)
        popup.title("Update Cashier")
        tk.Label(popup, text="Cashier Name").pack(pady=2)
        name = tk.Entry(popup)
        name.insert(0, old_uname)
        name.pack()
        tk.Label(popup, text="Password").pack(pady=2)
        password = tk.Entry(popup, show='*')
        password.insert(0, old_pwd)
        password.pack()
        tk.Button(popup, text="Save", command=save).pack(pady=5)

    def delete_cashier(self):
        selected = self.cashier_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a cashier to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this cashier?")
        if confirm:
            cashiers = read_file(CASHIERS_FILE)
            del cashiers[selected[0]]
            write_file(CASHIERS_FILE, cashiers)
            messagebox.showinfo("Deleted", "Cashier deleted successfully.")
            self.load_cashiers()

    def add_category(self):
        def save():
            entry = f"{category.get()}:{products.get()}"
            append_file(PRODUCTS_FILE, entry)
            messagebox.showinfo("Success", "Category added.")
            popup.destroy()

        popup = tk.Toplevel(self)
        popup.title("Add Product Category")
        tk.Label(popup, text="Category Name").pack(pady=2)
        category = tk.Entry(popup)
        category.pack()
        tk.Label(popup, text="10 Products (comma separated)").pack(pady=2)
        products = tk.Entry(popup)
        products.pack()
        tk.Button(popup, text="Save", command=save).pack(pady=5)


# --------------------- Cashier Panel ---------------------
class CashierPanel(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Cashier Panel")
        self.cart = []
        self.bill_total = 0

        tk.Label(self, text="Product Categories", font=('Arial', 14)).pack(pady=5)
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill='both', expand=True)

        for line in read_file(PRODUCTS_FILE):
            category, items = line.split(':')
            for item in items.split(','):
                self.listbox.insert('end', f"{category} - {item.strip()}")

        tk.Button(self, text="Add to Cart", command=self.add_to_cart).pack()
        tk.Button(self, text="Pay (Cash)", command=lambda: self.checkout('Cash')).pack()
        tk.Button(self, text="Pay (Card)", command=lambda: self.checkout('Card')).pack()

    def add_to_cart(self):
        selected = self.listbox.get(self.listbox.curselection())
        self.cart.append(selected)
        self.bill_total += 100  # assuming each item is 100 for simplicity
        messagebox.showinfo("Cart", f"Added {selected} to cart.")

    def checkout(self, method):
        total = self.bill_total
        if method == 'Card':
            total *= 0.9  # 10% discount

        append_file(BILLS_FILE, f"Bill {len(read_file(BILLS_FILE)) + 1}: {int(total)}")
        messagebox.showinfo("Payment Received", f"Payment complete. Total: {int(total)}")
        self.cart.clear()
        self.bill_total = 0
        

# --------------------- Login Panel ---------------------
class LoginPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Mart Management System")
        self.geometry("400x300")
        tk.Label(self, text="Login as Admin or Cashier", font=('Arial', 14)).pack(pady=20)

        tk.Button(self, text="Admin Login", command=self.admin_login).pack(fill='x', padx=50, pady=5)
        tk.Button(self, text="Cashier Login", command=self.cashier_login).pack(fill='x', padx=50, pady=5)

    def admin_login(self):
        def verify():
            creds = read_file(ADMIN_FILE)
            if f"{user.get()}:{pwd.get()}" in creds:
                messagebox.showinfo("Login", "Admin Login Successful")
                AdminPanel(self)
                popup.destroy()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        popup = tk.Toplevel(self)
        tk.Label(popup, text="Username").pack()
        user = tk.Entry(popup)
        user.pack()
        tk.Label(popup, text="Password").pack()
        pwd = tk.Entry(popup, show='*')
        pwd.pack()
        tk.Button(popup, text="Login", command=verify).pack()

    def cashier_login(self):
        def verify():
            creds = read_file(CASHIERS_FILE)
            if f"{user.get()}:{pwd.get()}" in creds:
                messagebox.showinfo("Login", "Cashier Login Successful")
                CashierPanel(self)
                popup.destroy()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        popup = tk.Toplevel(self)
        tk.Label(popup, text="Username").pack()
        user = tk.Entry(popup)
        user.pack()
        tk.Label(popup, text="Password").pack()
        pwd = tk.Entry(popup, show='*')
        pwd.pack()
        tk.Button(popup, text="Login", command=verify).pack()
        

# --------------------- Main ---------------------
if __name__ == '__main__':
    app = LoginPanel()
    app.mainloop()


