import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------- DB CONNECTION ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ra12@ji28", # CHANGE THIS to your Workbench password
        database="placement_db"
    )

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Placement Management System - MySQL Workbench")
root.geometry("900x600")

style = ttk.Style()
style.configure("TNotebook.Tab", padding=[20, 10], font=('Arial', 10, 'bold'))

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# ---------- TAB 1: STUDENTS ----------
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text=" Students ")

tk.Label(tab1, text="Name").grid(row=0, column=0, padx=10, pady=10)
tk.Label(tab1, text="Branch").grid(row=0, column=2, padx=10, pady=10)
tk.Label(tab1, text="CGPA").grid(row=1, column=0, padx=10, pady=10)
tk.Label(tab1, text="Password").grid(row=1, column=2, padx=10, pady=10)

e_name = tk.Entry(tab1, width=20); e_name.grid(row=0, column=1)
e_branch = tk.Entry(tab1, width=20); e_branch.grid(row=0, column=3)
e_cgpa = tk.Entry(tab1, width=20); e_cgpa.grid(row=1, column=1)
e_pass = tk.Entry(tab1, width=20, show="*"); e_pass.grid(row=1, column=3)

tree_stud = ttk.Treeview(tab1, columns=("ID","Name","Branch","CGPA"), show="headings")
for col in ("ID","Name","Branch","CGPA"):
    tree_stud.heading(col, text=col)
tree_stud.grid(row=3, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

def load_students():
    for i in tree_stud.get_children(): tree_stud.delete(i)
    db = get_db(); cur = db.cursor()
    cur.execute("SELECT student_id, name, branch, cgpa FROM students")
    for row in cur.fetchall():
        tree_stud.insert("", "end", values=row)
    db.close()

def add_student_gui():
    try:
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO students(name,branch,cgpa) VALUES(%s,%s,%s)",
                    (e_name.get(), e_branch.get(), float(e_cgpa.get())))
        db.commit(); db.close()
        messagebox.showinfo("Success", "Student Added!")
        load_students()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_student_gui():
    sel = tree_stud.selection()
    if not sel: return
    sid = tree_stud.item(sel[0])['values'][0]
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM students WHERE student_id=%s", (sid,))
    db.commit(); db.close()
    load_students()

ttk.Button(tab1, text="Add Student", command=add_student_gui).grid(row=2, column=1, pady=10)
ttk.Button(tab1, text="Refresh", command=load_students).grid(row=2, column=2)
ttk.Button(tab1, text="Delete Selected", command=delete_student_gui).grid(row=2, column=3)
load_students()

# ---------- TAB 2: COMPANIES ----------
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text=" Companies ")

tk.Label(tab2, text="Company Name").grid(row=0, column=0, padx=10, pady=10)
tk.Label(tab2, text="Role").grid(row=0, column=2, padx=10, pady=10)
tk.Label(tab2, text="Min CGPA").grid(row=1, column=0, padx=10, pady=10)

e_cname = tk.Entry(tab2, width=25); e_cname.grid(row=0, column=1)
e_role = tk.Entry(tab2, width=25); e_role.grid(row=0, column=3)
e_mincgpa = tk.Entry(tab2, width=25); e_mincgpa.grid(row=1, column=1)

tree_comp = ttk.Treeview(tab2, columns=("ID","Company","Role","MinCGPA"), show="headings")
for col in ("ID","Company","Role","MinCGPA"):
    tree_comp.heading(col, text=col)
tree_comp.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

def load_companies():
    for i in tree_comp.get_children(): tree_comp.delete(i)
    db = get_db(); cur = db.cursor()
    cur.execute("SELECT * FROM companies")
    for row in cur.fetchall(): tree_comp.insert("", "end", values=row)
    db.close()

def add_company_gui():
    db = get_db(); cur = db.cursor()
    cur.execute("INSERT INTO companies(company_name,role,min_cgpa) VALUES(%s,%s,%s)",
                (e_cname.get(), e_role.get(), float(e_mincgpa.get())))
    db.commit(); db.close()
    load_companies()
    messagebox.showinfo("Success", "Company Added!")

ttk.Button(tab2, text="Add Company", command=add_company_gui).grid(row=2, column=1, pady=10)
ttk.Button(tab2, text="Refresh", command=load_companies).grid(row=2, column=2)
load_companies()

# ---------- TAB 3: APPLICATIONS & ELIGIBILITY ----------
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text=" Applications ")

tk.Label(tab3, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
tk.Label(tab3, text="Company ID").grid(row=0, column=2, padx=10, pady=10)
e_sid = tk.Entry(tab3, width=15); e_sid.grid(row=0, column=1)
e_cid = tk.Entry(tab3, width=15); e_cid.grid(row=0, column=3)

tree_app = ttk.Treeview(tab3, columns=("AppID","Student","Company","Status"), show="headings")
for col in ("AppID","Student","Company","Status"):
    tree_app.heading(col, text=col)
tree_app.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

def load_apps():
    for i in tree_app.get_children(): tree_app.delete(i)
    db = get_db(); cur = db.cursor()
    cur.execute("""SELECT a.application_id, s.name, c.company_name, a.status
                   FROM applications a JOIN students s ON a.student_id=s.student_id
                   JOIN companies c ON a.company_id=c.company_id""")
    for r in cur.fetchall(): tree_app.insert("", "end", values=r)
    db.close()

def apply_gui():
    try:
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO applications(student_id, company_id) VALUES(%s,%s)", (e_sid.get(), e_cid.get()))
        db.commit(); db.close()
        messagebox.showinfo("Success", "Applied Successfully!")
        load_apps()
    except Exception as e:
        messagebox.showerror("Error", f"Already applied or wrong ID\n{e}")

def check_eligible_gui():
    try:
        db = get_db(); cur = db.cursor()
        cur.execute("SELECT cgpa FROM students WHERE student_id=%s", (e_sid.get(),))
        res = cur.fetchone()
        if not res:
            messagebox.showerror("Error", "Student not found")
            return
        cgpa = res[0]
        cur.execute("SELECT company_id, company_name, role FROM companies WHERE min_cgpa<=%s", (cgpa,))
        rows = cur.fetchall()
        msg = f"Your CGPA: {cgpa}\n\nEligible:\n" + "\n".join([f"{r[0]} - {r[1]} ({r[2]})" for r in rows])
        messagebox.showinfo("Eligible Companies", msg if rows else "No eligible companies")
        db.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

ttk.Button(tab3, text="Apply Job", command=apply_gui).grid(row=1, column=1, pady=10)
ttk.Button(tab3, text="Check Eligibility", command=check_eligible_gui).grid(row=1, column=2)
ttk.Button(tab3, text="Refresh", command=load_apps).grid(row=1, column=3)
load_apps()

# ---------- TAB 4: REPORT ----------
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text=" Report ")

report_label = tk.Label(tab4, text="", font=("Arial", 14), justify="left")
report_label.pack(pady=30)

def load_report():
    db = get_db(); cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM students"); total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM applications WHERE status='Placed'"); placed = cur.fetchone()[0]
    cur.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
    stats = cur.fetchall()
    db.close()
    text = f"Total Students: {total}\nTotal Placed Applications: {placed}\n\nBreakdown:\n"
    for s,c in stats: text += f" {s}: {c}\n"
    report_label.config(text=text)

ttk.Button(tab4, text="Load Dashboard", command=load_report).pack()
load_report()

root.mainloop()