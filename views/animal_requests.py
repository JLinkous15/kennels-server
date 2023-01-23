import sqlite3
import json
from models import Animal, Location, Customer
from .location_requests import get_single_location
from .customer_requests import get_single_customer

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted"
    }
]

def get_all_animals(query_params):
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""
        where_clause = ""

        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "_sortBy":
                if qs_value == 'location':
                    sort_by = " ORDER BY location_id"
                if qs_value == "customer":
                    sort_by = "ORDER BY customer_id"
                if qs_value == 'status':
                    sort_by = 'ORDER BY status ASC'
                if qs_value == 'name':
                    sort_by = 'ORDER BY a.name ASC'
            elif qs_key == "locationId":
                where_clause = f"WHERE a.location_id = {qs_value}"
            elif qs_key == "status":
                where_clause = f"WHERE a.status = \"{qs_value}\""

        sql_to_execute = f"""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            l.name location_name,
            l.address location_address,
            a.customer_id,
            c.name AS customer_name,
            c.address AS customer_address,
            c.email AS customer_email
        FROM Animal a
        JOIN `Location` l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        {where_clause}
        {sort_by}
        """

        # Write the SQL query to get the information you want
        db_cursor.execute(sql_to_execute)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['breed'],row['status'], row['location_id'],row['customer_id'])

            location = Location(row["location_id"], row["location_name"], row["location_address"])

            customer = Customer(row["customer_id"], row["customer_name"], row["customer_address"], row["customer_email"])
            
            animal.location = location.__dict__

            animal.customer = customer.__dict__
                          
            animals.append(animal.__dict__)

    return animals

    # Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return animal.__dict__

def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return new_animal

def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_animals_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
        FROM animal a
        WHERE a.location_id = ?
        """, ( location_id, ))

        animals = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            animal = Animal(row["id"],row["name"],row["status"],row["breed"],row["customer_id"],row["location_id"])
            animals.append(animal.__dict__)
        return animals

def get_animals_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
        FROM animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            animal = Animal(row["id"],row["name"],row["status"],row["breed"],row["customer_id"],row["location_id"])
            animals.append(animal.__dict__)
        return animals