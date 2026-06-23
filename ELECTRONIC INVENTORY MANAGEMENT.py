import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from PIL import Image, ImageTk
# =========================
# GLOBAL VARIABLES
# =========================

inventory = {}
DATA_FILE = "inventory.json"

# =========================
# FILE HANDLING
# =========================

def save_data():
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(inventory, file, indent=4)

        messagebox.showinfo("Success", "Data saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_data():
    global inventory

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                inventory = json.load(file)

            refresh_table()

        except:
            inventory = {}

# =========================
# LOGIN FUNCTION
# =========================
def check_login():

    staff_id = staff_id_entry.get().strip()
    password = password_entry.get().strip()

    if staff_id in STAFF_ACCOUNTS and STAFF_ACCOUNTS[staff_id] == password:

        messagebox.showinfo("Success", "Login Successful")

        login_window.destroy()

        root.deiconify()      # Paparkan inventory system

    else:

        messagebox.showerror(
            "Login Failed",
            "Wrong Staff ID or Password"
        )
        

# =========================
# TABLE FUNCTIONS
# =========================

def refresh_table():
    for row in inventory_table.get_children():
        inventory_table.delete(row)

    for item_id, data in inventory.items():
        inventory_table.insert(
            "",
            "end",
            values=(
                item_id,
                data["name"],
                data["category"],
                data["quantity"],
                data["price"]
            )
        )


# =========================
# CLEAR INPUT
# =========================

def clear_fields():
    item_id_entry.delete(0, tk.END)
    item_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    category_combo.set("")


# =========================
# ADD ITEM
# =========================

def add_item():

    item_id = item_id_entry.get().strip()
    name = item_name_entry.get().strip()
    category = category_combo.get().strip()
    quantity = quantity_entry.get().strip()
    price = price_entry.get().strip()

    if not item_id or not name or not category or not quantity or not price:
        messagebox.showerror("Error", "Please fill all fields")
        return

    if item_id in inventory:
        messagebox.showerror("Error", "Item ID already exists")
        return

    try:
        quantity = int(quantity)
        price = float(price)

        if quantity < 0 or price < 0:
            raise ValueError

    except:
        messagebox.showerror(
            "Error",
            "Quantity and Price must be positive numbers"
        )
        return

    inventory[item_id] = {
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": price
    }

    refresh_table()
    clear_fields()

    messagebox.showinfo("Success", "Item added successfully")


# =========================
# UPDATE ITEM
# =========================

def update_item():

    item_id = item_id_entry.get().strip()

    if item_id not in inventory:
        messagebox.showerror("Error", "Item not found")
        return

    try:

        inventory[item_id]["name"] = item_name_entry.get()
        inventory[item_id]["category"] = category_combo.get()
        inventory[item_id]["quantity"] = int(quantity_entry.get())
        inventory[item_id]["price"] = float(price_entry.get())

        refresh_table()

        messagebox.showinfo(
            "Success",
            "Item updated successfully"
        )

    except:
        messagebox.showerror(
            "Error",
            "Invalid input"
        )


# =========================
# DELETE ITEM
# =========================

def delete_item():

    item_id = item_id_entry.get().strip()

    if item_id in inventory:

        confirm = messagebox.askyesno(
            "Delete",
            "Are you sure?"
        )

        if confirm:

            del inventory[item_id]

            refresh_table()
            clear_fields()

            messagebox.showinfo(
                "Success",
                "Item deleted successfully"
            )

    else:
        messagebox.showerror(
            "Error",
            "Item not found"
        )


# =========================
# SEARCH ITEM
# =========================

def search_item():

    item_id = item_id_entry.get().strip()

    if item_id not in inventory:
        messagebox.showerror("Error", "Item not found")
        return

    # Ambil data item
    data = inventory[item_id]

    # Paparkan data dalam input field
    item_name_entry.delete(0, tk.END)
    item_name_entry.insert(0, data["name"])

    category_combo.set(data["category"])

    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, data["quantity"])

    price_entry.delete(0, tk.END)
    price_entry.insert(0, data["price"])

    # Cari dan highlight dalam table
    for row in inventory_table.get_children():

        values = inventory_table.item(row, "values")

        if values[0] == item_id:
            # Buang selection lama
            inventory_table.selection_remove(
                inventory_table.selection()
            )

            # Highlight baris yang dijumpai
            inventory_table.selection_set(row)
            inventory_table.focus(row)
            inventory_table.see(row)

            break

    messagebox.showinfo(
        "Success",
        f"Item '{item_id}' found and highlighted."
    )


# =========================
# LOW STOCK ALERT
# =========================

def low_stock_alert():

    low_stock_items = []

    for item_id, data in inventory.items():

        if data["quantity"] < 20:

            low_stock_items.append(
                f"{item_id} - {data['name']} ({data['quantity']} units)"
            )

    if low_stock_items:

        result = "\n".join(low_stock_items)

        messagebox.showwarning(
            "Low Stock Alert",
            result
        )

    else:

        messagebox.showinfo(
            "Stock Status",
            "No low stock items"
        )


# ====================================================================================================
#                               GUI WINDOW
# ====================================================================================================

root = tk.Tk()
root.withdraw()   #<-------untuk sorokkan inventory,jika user belom letak password/password salah
# =========================
# BACKGROUND IMAGE
# =========================
bg_image = Image.open("Background.jpeg")  
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))

bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label.image = bg_photo
# =========================
# LOGO IMAGE
# =========================
logo_image = Image.open("LogoCompany.png ")
logo_image = logo_image.resize((200, 120))

logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo, bg="white")
logo_label.pack(pady=5)
logo_label.image = logo_photo

root.title("Electronic Inventory Management System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="Electronic Inventory Management System",
    font=("Arial", 18, "bold"),
    bg="white",
    
)

title_label.pack(pady=10)

# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(root,bg="white")
input_frame.pack(pady=10)

# Item ID

tk.Label(
    input_frame,
    text="Item ID",
    bg="white"
).grid(row=0, column=0, padx=10, pady=5)

item_id_entry = tk.Entry(input_frame,bg="silver")
item_id_entry.grid(row=0, column=1)

# Item Name

tk.Label(
    input_frame,
    text="Item Name",
    bg="white"
).grid(row=1, column=0, padx=10, pady=5)

item_name_entry = tk.Entry(input_frame,bg="silver")
item_name_entry.grid(row=1, column=1)

# Category

tk.Label(
    input_frame,
    text="Category",
    bg="white"
).grid(row=2, column=0, padx=10, pady=5)

category_combo = ttk.Combobox(
    input_frame,
    values=[
        "Laptop",
        "Monitor",
        "Printer",
        "Keyboard",
        "Mouse",
        "Router",
        "Projector",
        "Television",
        "Headphone"

    ]
)

category_combo.grid(row=2, column=1)

# Quantity

tk.Label(
    input_frame,
    text="Quantity",
    bg="white"
).grid(row=3, column=0, padx=10, pady=5)

quantity_entry = tk.Entry(input_frame,bg="silver")
quantity_entry.grid(row=3, column=1)

# Price

tk.Label(
    input_frame,
    text="Price",
    bg="white"
).grid(row=4, column=0, padx=10, pady=5)

price_entry = tk.Entry(input_frame,bg="silver")
price_entry.grid(row=4, column=1)

# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Add Item",
    command=add_item
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update Item",
    command=update_item
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete Item",
    command=delete_item
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Search Item",
    command=search_item
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame,
    text="Low Stock Alert",
    command=low_stock_alert
).grid(row=0, column=4, padx=5)

tk.Button(
    button_frame,
    text="Save Data",
    bg="#3964ba",
    font=("Arial", 10, "bold"),
    width=12,
    height=2,
    fg="white",
    command=save_data
).grid(row=0, column=5, padx=(25, 5))

# =========================
# TABLE
# =========================

table_frame = tk.Frame(root)
table_frame.pack(pady=20)

inventory_table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Name",
        "Category",
        "Quantity",
        "Price"
    ),
    show="headings",
    height=15
)

inventory_table.heading("ID", text="Item ID")
inventory_table.heading("Name", text="Item Name")
inventory_table.heading("Category", text="Category")
inventory_table.heading("Quantity", text="Quantity")
inventory_table.heading("Price", text="Price")

inventory_table.column("ID", width=120)
inventory_table.column("Name", width=250)
inventory_table.column("Category", width=150)
inventory_table.column("Quantity", width=120)
inventory_table.column("Price", width=120)

inventory_table.pack()

# ===========================================================================
#                          LOGIN WINDOW
# ===========================================================================

login_window = tk.Toplevel()
bg_image = Image.open("LOGO LOGIN.webp")  
bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()))
# =========================
# LOGO IMAGE
# =========================
logo_image = Image.open("LogoCompany.png ")  
logo_image = logo_image.resize((200, 200))   
logo_photo = ImageTk.PhotoImage(logo_image)

# =========================
# BACKGROUND IMAGE
# =========================
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(login_window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label.image = bg_photo

login_window.title("Staff Login")

login_window.state("zoomed")

login_window.protocol("WM_DELETE_WINDOW", root.destroy)

logo_label = tk.Label(
    login_window,
    image=logo_photo,
    bg="Black"
)
logo_label.pack(pady=15)

logo_label.image = logo_photo

tk.Label(
    login_window,
    text="ELEC PRIME INVENTORY",
    bg="white",
    font=("Times New Roman",45, "bold italic")
).pack(pady=100)

tk.Label(
    login_window,
    text="Staff ID",
    font=("Arial",15,"bold")
).pack(pady=20)

staff_id_entry = tk.Entry(
    login_window,
    bg="silver",        
    fg="black",        
    insertbackground="black",  
    font=("Arial", 12)
)
staff_id_entry.pack()

tk.Label(
    login_window,
    text="Password",
    font=("Arial",15,"bold")
).pack(pady=20)

password_entry = tk.Entry(
    login_window,
    show="*",
    bg="silver",
    fg="black",
    insertbackground="black",
    font=("Arial", 12)
)
password_entry.pack()

tk.Button(
    login_window,
    text="Login",
    bg="#3964ba",
    font=("Arial",15,),
    command=check_login
).pack(pady=15)


# =========================
# STAFF ACCOUNT
# =========================
STAFF_ACCOUNTS = {
    "admin": "1234",
    "staff": "password",
    "hairil": "12345"
}

# =========================
# LOAD DATA
# =========================

load_data()

# =========================
# RUN
# =========================

root.mainloop()           