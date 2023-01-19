import json
import sqlite3
from models import Employee, Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]

def get_all_employees():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            e.id,
            e.name,
            e.address home_address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN location l
            ON l.id = e.location_id
        """)

    employees = []

    dataset = db_cursor.fetchall()

    for row in dataset:
        employee = Employee(row["id"], row["name"], row["home_address"], row["location_id"])

        location = Location(row["id"], row["location_name"], row["location_address"])

        employee.location = location.__dict__

        employees.append(employee.__dict__)
    return employees

def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT *
        FROM employee a
        WHERE a.id=?
        """, (id, ))
        
        data=db_cursor.fetchone()

        employee = Employee(data["id"], data["name"], data["address"],  data["location_id"])

        return employee.__dict__

def create_employee(employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            (name, address, location_id)
        VALUES( ?, ?, ? );
        """, (employee["name"], employee["address"], employee["location_id"]))

        id = db_cursor.lastrowid

        employee["id"] = id

def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index

    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Employee
            SET
                name = ?,
                address = ?,
                location_id = ?
        WHERE id = ?
        """, (new_employee["name"], new_employee["address"], new_employee["location_id"], id))

        rows_affected = db_cursor.rowcount
    
    if rows_affected == 0:
        return False
    else:
        return True

def get_employees_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
        FROM employee a
        WHERE a.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row["id"],row["name"],row["address"],row["location_id"])
            employees.append(employee.__dict__)
        return employees