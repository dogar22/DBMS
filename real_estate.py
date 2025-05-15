import customtkinter as ctk
import pymysql
from tkinter import messagebox

# Configure CTk
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# MySQL Connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="2004",
    database="restate",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()

# Create Table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255),
    owner VARCHAR(255),
    size INT,
    value INT
)
''')

# App Window
app = ctk.CTk()
app.title("Real Estate Management System")
app.geometry("700x500")

# Entry Fields
name_entry = ctk.CTkEntry(app, placeholder_text="Property Name")
name_entry.pack(pady=5)

location_entry = ctk.CTkEntry(app, placeholder_text="Location")
location_entry.pack(pady=5)

owner_entry = ctk.CTkEntry(app, placeholder_text="Owner")
owner_entry.pack(pady=5)

size_entry = ctk.CTkEntry(app, placeholder_text="Size (sq ft)")
size_entry.pack(pady=5)

value_entry = ctk.CTkEntry(app, placeholder_text="Value ($)")
value_entry.pack(pady=5)

# Functions
def add_property():
    name = name_entry.get()
    location = location_entry.get()
    owner = owner_entry.get()
    size = size_entry.get()
    value = value_entry.get()
    if name and location and owner and size and value:
        cursor.execute("INSERT INTO property (name, location, owner, size, value) VALUES (%s, %s, %s, %s, %s)",
                       (name, location, owner, size, value))
        conn.commit()
        messagebox.showinfo("Success", "Property Added!")
        show_properties()
    else:
        messagebox.showerror("Error", "All fields required")

def show_properties():
    cursor.execute("SELECT * FROM property")
    records = cursor.fetchall()
    listbox.delete("1.0", ctk.END)
    for row in records:
        listbox.insert(ctk.END, f"ID: {row['property_id']} | Name: {row['name']} | Location: {row['location']} | Owner: {row['owner']} | Size: {row['size']} | Value: ${row['value']}\n")

def delete_property():
    selected_text = listbox.get("insert linestart", "insert lineend")
    if selected_text:
        prop_id = selected_text.split('|')[0].split(':')[1].strip()
        cursor.execute("DELETE FROM property WHERE property_id = %s", (prop_id,))
        conn.commit()
        show_properties()
        messagebox.showinfo("Deleted", "Property removed.")

def update_property():
    selected_text = listbox.get("insert linestart", "insert lineend")
    if selected_text:
        prop_id = selected_text.split('|')[0].split(':')[1].strip()
        name = name_entry.get()
        location = location_entry.get()
        owner = owner_entry.get()
        size = size_entry.get()
        value = value_entry.get()
        cursor.execute("""
            UPDATE property SET name=%s, location=%s, owner=%s, size=%s, value=%s WHERE property_id=%s
        """, (name, location, owner, size, value, prop_id))
        conn.commit()
        show_properties()
        messagebox.showinfo("Updated", "Property updated.")

# Buttons
add_btn = ctk.CTkButton(app, text="Add Property", command=add_property)
add_btn.pack(pady=5)

update_btn = ctk.CTkButton(app, text="Update Property", command=update_property)
update_btn.pack(pady=5)

delete_btn = ctk.CTkButton(app, text="Delete Property", command=delete_property)
delete_btn.pack(pady=5)

# Listbox for showing properties
listbox = ctk.CTkTextbox(app, height=200, width=600)
listbox.pack(pady=10)

# Show initial data
show_properties()

# Run the app
app.mainloop()

# Close MySQL connection on exit
cursor.close()
conn.close()

