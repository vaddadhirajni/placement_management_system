import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ra12@ji28",
    database="placements_db"
)

cursor = db.cursor()

# ---------------- STUDENT ---------------- #

def add_student():
    name = input("Name: ")
    branch = input("Branch: ")
    cgpa = float(input("CGPA: "))
    password = input("Password: ")

    sql = """
    INSERT INTO students(name,branch,cgpa,password)
    VALUES(%s,%s,%s,%s)

    cursor.execute(sql,(name,branch,cgpa,password))
    db.commit()

    print("Student Added Successfully")

def view_students():
    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    for row in data:
        print(row)

def delete_student():
    sid = int(input("Student ID: "))

    cursor.execute(
        "DELETE FROM students WHERE student_id=%s",
        (sid,)
    )

    db.commit()

    print("Student Deleted")

# ---------------- COMPANY ---------------- #

def add_company():

    cname = input("Company Name: ")
    role = input("Role: ")
    mincgpa = float(input("Minimum CGPA: "))

    sql = """
    INSERT INTO companies(company_name,role,min_cgpa)
    VALUES(%s,%s,%s)
    """

    cursor.execute(sql,(cname,role,mincgpa))
    db.commit()

    print("Company Added")

def view_companies():

    cursor.execute("SELECT * FROM companies")

    for row in cursor.fetchall():
        print(row)

def search_company():

    name = input("Company Name: ")

    cursor.execute(
        "SELECT * FROM companies WHERE company_name LIKE %s",
        ('%' + name + '%',)
    )

    for row in cursor.fetchall():
        print(row)

# ---------------- LOGIN ---------------- #

def login():

    sid = input("Student ID: ")
    password = input("Password: ")

    query = """
    SELECT * FROM students
    WHERE student_id=%s
    AND password=%s
    """

    cursor.execute(query,(sid,password))

    result = cursor.fetchone()

    if result:
        print("Login Successful")
    else:
        print("Invalid Login")

# ---------------- ELIGIBILITY ---------------- #

def eligible_companies():

    sid = int(input("Student ID: "))

    cursor.execute(
        "SELECT cgpa FROM students WHERE student_id=%s",
        (sid,)
    )

    result = cursor.fetchone()

    if result is None:
        print("Student Not Found")
        return

    cgpa = result[0]

    cursor.execute(
        "SELECT * FROM companies WHERE min_cgpa<=%s",
        (cgpa,)
    )

    print("\nEligible Companies")

    for row in cursor.fetchall():
        print(row)

# ---------------- APPLICATION ---------------- #

def apply_job():

    sid = int(input("Student ID: "))
    cid = int(input("Company ID: "))

    sql = """
    INSERT INTO applications(student_id,company_id)
    VALUES(%s,%s)
    """

    cursor.execute(sql,(sid,cid))
    db.commit()

    print("Application Submitted")

def view_applications():

    cursor.execute("SELECT * FROM applications")

    for row in cursor.fetchall():
        print(row)

def update_status():

    aid = int(input("Application ID: "))
    status = input("Status: ")

    sql = """
    UPDATE applications
    SET status=%s
    WHERE application_id=%s
    """

    cursor.execute(sql,(status,aid))
    db.commit()

    print("Status Updated")

# ---------------- REPORT ---------------- #

def placement_report():

    cursor.execute("""
    SELECT status,COUNT(*)
    FROM applications
    GROUP BY status
    """)

    print("\nPlacement Statistics")

    for row in cursor.fetchall():
        print(row)

# ---------------- MENU ---------------- #

while True:

    print("\n===== Placement Management System =====")
    print("1.Add Student")
    print("2.View Students")
    print("3.Delete Student")
    print("4.Student Login")
    print("5.Add Company")
    print("6.View Companies")
    print("7.Search Company")
    print("8.Eligible Companies")
    print("9.Apply Job")
    print("10.View Applications")
    print("11.Update Status")
    print("12.Placement Report")
    print("13.Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        delete_student()

    elif choice == "4":
        login()

    elif choice == "5":
        add_company()

    elif choice == "6":
        view_companies()

    elif choice == "7":
        search_company()

    elif choice == "8":
        eligible_companies()

    elif choice == "9":
        apply_job()

    elif choice == "10":
        view_applications()

    elif choice == "11":
        update_status()

    elif choice == "12":
        placement_report()

    elif choice == "13":
        print("Thank You")
        break

    else:
        print("Invalid Choice")