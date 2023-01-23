import json
import sqlite3
from models import Location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations(query_params):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor=conn.cursor()

        group_by = ["",""]

        if len(query_params)==0:
            group_by[0] = "COUNT(*) AS animals"
            group_by[1] = "GROUP BY a.location_id"

        to_be_executed = f"""
        SELECT 
            l.id,
            l.name,
            l.address,
            a.location_id,
            {group_by[0]}
        FROM location l
        JOIN animal a ON a.location_id = l.id
        {group_by[1]}
        """

        db_cursor.execute(to_be_executed)
        locations = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row["id"], row["name"], row["address"])
            location.animals = (row["animals"])
            locations.append(location.__dict__)
        return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory=sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT *
        FROM location a
        WHERE a.id=?
        """, (id, ))

        data=db_cursor.fetchone()

        location = Location(data["id"], data["name"], data["address"])

        return location.__dict__

def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)

    return location

def delete_location(id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index

    if location_index >= 0:
        LOCATIONS.pop(location_index)

def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location["name"], new_location["address"], id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True