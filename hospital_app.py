import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("hospital_equipment.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS department (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vendor (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    category TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT,
    serial_number TEXT,
    model_no TEXT,
    manufacturer TEXT,
    department TEXT,
    purchase_date TEXT,
    expiry_date TEXT,
    status TEXT,
    vendor_id INTEGER,
    vendor_contact TEXT,
    vendor_email TEXT,
    quantity INTEGER,
    FOREIGN KEY(vendor_id) REFERENCES vendor(vendor_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issue_report (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT,
    serial_number TEXT,
    manufacturer TEXT,
    issue_type TEXT,
    problem_description TEXT,
    media_path TEXT,
    date_raised TEXT,
    status TEXT,
    technician TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS discard_equipment (
    discard_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT,
    serial_number TEXT,
    model_no TEXT,
    reason TEXT,
    media_path TEXT,
    date TEXT
)
""")

conn.commit()

# ---------------- MAIN APP ----------------
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Equipment Management")
        self.root.geometry("1350x650")

        # Tabs
        self.tab_control = ttk.Notebook(root)
        
        self.dashboard_tab = ttk.Frame(self.tab_control)
        self.equipment_tab = ttk.Frame(self.tab_control)
        self.issue_tab = ttk.Frame(self.tab_control)
        self.vendor_tab = ttk.Frame(self.tab_control)
        self.discard_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.dashboard_tab, text="Dashboard")
        self.tab_control.add(self.equipment_tab, text="Equipment")
        self.tab_control.add(self.issue_tab, text="Issue Reports")
        self.tab_control.add(self.vendor_tab, text="Vendors")
        self.tab_control.add(self.discard_tab, text="Discarded")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_dashboard()
        self.setup_equipment_tab()
        self.setup_issue_tab()
        self.setup_vendor_tab()
        self.setup_discard_tab()

    # ---------------- DASHBOARD ----------------
    def setup_dashboard(self):
        frame = self.dashboard_tab
        stats = {
            "Total Equipment": "SELECT COUNT(*) FROM equipment",
            "Working": "SELECT COUNT(*) FROM equipment WHERE status='Working'",
            "Under Maintenance": "SELECT COUNT(*) FROM equipment WHERE status='Under repair'",
            "Expired": "SELECT COUNT(*) FROM equipment WHERE expiry_date <= date('now')",
            "Discarded": "SELECT COUNT(*) FROM discard_equipment",
            "Departments": "SELECT COUNT(*) FROM department"
        }
        row = 0
        for key, query in stats.items():
            cursor.execute(query)
            count = cursor.fetchone()[0]
            label = tk.Label(frame, text=f"{key}: {count}", font=("Arial", 14), relief="ridge", padx=10, pady=10)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            row += 1

    # ---------------- EQUIPMENT TAB ----------------
    def setup_equipment_tab(self):
        frame = self.equipment_tab
        form_frame = tk.LabelFrame(frame, text="Add / Update Equipment")
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Equipment Name", "Serial Number", "Model No", "Manufacturer", "Department", 
                  "Purchase Date (YYYY-MM-DD)", "Expiry Date (YYYY-MM-DD)", "Status", 
                  "Vendor ID", "Vendor Contact", "Vendor Email", "Quantity"]
        self.equipment_entries = {}
        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(form_frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.equipment_entries[text] = entry

        tk.Button(form_frame, text="Add Equipment", command=self.add_equipment).grid(row=len(labels), column=0, columnspan=2, pady=10)

        table_frame = tk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("ID","Equipment Name","Serial Number","Model No","Manufacturer","Department",
                   "Purchase Date","Expiry Date","Status","Vendor ID","Vendor Contact","Vendor Email","Quantity")
        self.equipment_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.equipment_table.heading(col, text=col)
        self.equipment_table.pack(fill="both", expand=True)
        self.load_equipment_table()

    def add_equipment(self):
        values = {key: entry.get() for key, entry in self.equipment_entries.items()}
        cursor.execute("""
            INSERT INTO equipment (equipment_name, serial_number, model_no, manufacturer, department, purchase_date, expiry_date, status, vendor_id, vendor_contact, vendor_email, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (values["Equipment Name"], values["Serial Number"], values["Model No"], values["Manufacturer"],
              values["Department"], values["Purchase Date (YYYY-MM-DD)"], values["Expiry Date (YYYY-MM-DD)"],
              values["Status"], values["Vendor ID"], values["Vendor Contact"], values["Vendor Email"], values["Quantity"]))
        conn.commit()
        messagebox.showinfo("Success", "Equipment added successfully!")
        self.load_equipment_table()

    def load_equipment_table(self):
        for row in self.equipment_table.get_children():
            self.equipment_table.delete(row)
        cursor.execute("SELECT * FROM equipment")
        for row in cursor.fetchall():
            self.equipment_table.insert("", "end", values=row)

    # ---------------- ISSUE TAB ----------------
    def setup_issue_tab(self):
        frame = self.issue_tab
        form_frame = tk.LabelFrame(frame, text="Add Issue Report")
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Equipment Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_name = tk.Entry(form_frame, width=40)
        self.issue_entries_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Serial Number").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_serial = tk.Entry(form_frame, width=40)
        self.issue_entries_serial.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Manufacturer").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_manufact = tk.Entry(form_frame, width=40)
        self.issue_entries_manufact.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Issue Type").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.issue_type_cb = ttk.Combobox(form_frame, values=["Technical Issue", "Mechanical Issue", "Electrical Issue", "User Operation"], state="readonly", width=37)
        self.issue_type_cb.grid(row=3, column=1, padx=5, pady=5)
        self.issue_type_cb.current(0)

        tk.Label(form_frame, text="Problem Description").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_problem = tk.Entry(form_frame, width=50)
        self.issue_entries_problem.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Media File Path").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_media = tk.Entry(form_frame, width=50)
        self.issue_entries_media.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Browse Media", command=self.browse_media).grid(row=5, column=2, padx=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD)").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_date = tk.Entry(form_frame, width=40)
        self.issue_entries_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Status").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_status = tk.Entry(form_frame, width=40)
        self.issue_entries_status.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Technician").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.issue_entries_tech = tk.Entry(form_frame, width=40)
        self.issue_entries_tech.grid(row=8, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Add Issue", command=self.add_issue).grid(row=9, column=0, columnspan=3, pady=10)

        table_frame = tk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("ID","Equipment Name","Serial Number","Manufacturer","Issue Type","Problem","Media","Date","Status","Technician")
        self.issue_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.issue_table.heading(col, text=col)
        self.issue_table.pack(fill="both", expand=True)
        self.load_issue_table()

    def browse_media(self):
        filepath = filedialog.askopenfilename(filetypes=[("Media files", "*.jpg *.png *.mp4 *.avi *.mov")])
        if filepath:
            self.issue_entries_media.delete(0, tk.END)
            self.issue_entries_media.insert(0, filepath)

    def add_issue(self):
        cursor.execute("""
            INSERT INTO issue_report (equipment_name, serial_number, manufacturer, issue_type, problem_description, media_path, date_raised, status, technician)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.issue_entries_name.get(), self.issue_entries_serial.get(), self.issue_entries_manufact.get(),
              self.issue_type_cb.get(), self.issue_entries_problem.get(), self.issue_entries_media.get(),
              self.issue_entries_date.get(), self.issue_entries_status.get(), self.issue_entries_tech.get()))
        conn.commit()
        messagebox.showinfo("Success", "Issue added successfully!")
        self.load_issue_table()

    def load_issue_table(self):
        for row in self.issue_table.get_children():
            self.issue_table.delete(row)
        cursor.execute("SELECT * FROM issue_report")
        for row in cursor.fetchall():
            self.issue_table.insert("", "end", values=row)

    # ---------------- VENDOR TAB ----------------
    def setup_vendor_tab(self):
        frame = self.vendor_tab
        form_frame = tk.LabelFrame(frame, text="Add Vendor")
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Name", "Phone", "Email", "Address", "Category"]
        self.vendor_entries = {}
        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.vendor_entries[text] = entry

        tk.Button(form_frame, text="Add Vendor", command=self.add_vendor).grid(row=len(labels), column=0, columnspan=2, pady=10)

        table_frame = tk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("ID","Name","Phone","Email","Address","Category")
        self.vendor_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.vendor_table.heading(col, text=col)
        self.vendor_table.pack(fill="both", expand=True)
        self.load_vendor_table()

    def add_vendor(self):
        values = {key: entry.get() for key, entry in self.vendor_entries.items()}
        cursor.execute("""
            INSERT INTO vendor (vendor_name, phone, email, address, category)
            VALUES (?, ?, ?, ?, ?)
        """, (values["Name"], values["Phone"], values["Email"], values["Address"], values["Category"]))
        conn.commit()
        messagebox.showinfo("Success", "Vendor added successfully!")
        self.load_vendor_table()

    def load_vendor_table(self):
        for row in self.vendor_table.get_children():
            self.vendor_table.delete(row)
        cursor.execute("SELECT * FROM vendor")
        for row in cursor.fetchall():
            self.vendor_table.insert("", "end", values=row)

    # ---------------- DISCARD TAB ----------------
    def setup_discard_tab(self):
        frame = self.discard_tab
        form_frame = tk.LabelFrame(frame, text="Discard Equipment")
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Equipment Name", "Serial Number", "Model No", "Reason", "Media Path", "Date (YYYY-MM-DD)"]
        self.discard_entries = {}
        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.discard_entries[text] = entry

        tk.Button(form_frame, text="Browse Media", command=self.browse_discard_media).grid(row=4, column=2, padx=5)
        tk.Button(form_frame, text="Discard Equipment", command=self.add_discard).grid(row=len(labels), column=0, columnspan=3, pady=10)

        table_frame = tk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("ID","Equipment Name","Serial Number","Model No","Reason","Media Path","Date")
        self.discard_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.discard_table.heading(col, text=col)
        self.discard_table.pack(fill="both", expand=True)
        self.load_discard_table()

    def browse_discard_media(self):
        filepath = filedialog.askopenfilename(filetypes=[("Media files", "*.jpg *.png *.mp4 *.avi *.mov")])
        if filepath:
            self.discard_entries["Media Path"].delete(0, tk.END)
            self.discard_entries["Media Path"].insert(0, filepath)

    def add_discard(self):
        values = {key: entry.get() for key, entry in self.discard_entries.items()}
        cursor.execute("""
            INSERT INTO discard_equipment (equipment_name, serial_number, model_no, reason, media_path, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (values["Equipment Name"], values["Serial Number"], values["Model No"],
              values["Reason"], values["Media Path"], values["Date (YYYY-MM-DD)"]))
        conn.commit()
        messagebox.showinfo("Success", "Equipment discarded successfully!")
        self.load_discard_table()

    def load_discard_table(self):
        for row in self.discard_table.get_children():
            self.discard_table.delete(row)
        cursor.execute("SELECT * FROM discard_equipment")
        for row in cursor.fetchall():
            self.discard_table.insert("", "end", values=row)

# ---------------- RUN APP ----------------
root = tk.Tk()
app = HospitalApp(root)
root.mainloop()
