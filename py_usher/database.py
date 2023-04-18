import sqlite3
import json


class DBHandler:
    def __init__(self):
        try:
            DBHandler.create_table()
        except sqlite3.OperationalError:
            pass

    @staticmethod
    def create_table() -> dict:
        conn = sqlite3.connect("py_usher.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE event_types (
            id INTEGER PRIMARY KEY,
            event_name TEXT,
            operations TEXT
            )""")
        conn.commit()
        conn.close()
        return {"message": "db file initialized."}

    @staticmethod
    def fetch_event(event_type: str) -> tuple or None:
        conn = sqlite3.connect("py_usher.db")
        c = conn.cursor()
        c.execute("SELECT * FROM event_types WHERE event_name = ?", (event_type,))
        event = c.fetchone()
        conn.close()
        if event:
            return event
        else:
            return None

    @staticmethod
    def insert_new(event_type: str, func_name: str) -> dict:
        event = DBHandler.fetch_event(event_type)
        conn = sqlite3.connect("py_usher.db")
        c = conn.cursor()
        if not event:
            operations = {"operations": [func_name]}
            c.execute("INSERT INTO event_types (event_name, operations) VALUES (?, ?)",
                      (event_type, json.dumps(operations)))
            conn.commit()
            conn.close()
            return {"message": f"New event type {event_type} created. {func_name} added to its operations.",
                    "status_code": 201}

        operations_list = list(json.loads(event[2])['operations'])
        if func_name not in operations_list:
            updated_op = {"operations": operations_list}
            updated_op['operations'].append(func_name)
            c.execute("UPDATE event_types SET operations = ? WHERE id = ?", (json.dumps(updated_op), event[0]))
            conn.commit()
            conn.close()
            return {"message": f"Operation {func_name} added to event type {event_type}.",
                    "status_code": 201}
        conn.commit()
        conn.close()
        return {"message": f"Operation {func_name} already exists in event type {event_type}."}

    @staticmethod
    def del_operation(event_type: str, func_name: str) -> dict:
        conn = sqlite3.connect("py_usher.db")
        c = conn.cursor()
        event = DBHandler.fetch_event(event_type)
        if not event:
            return {"message": "No such event type in the db."}
        operations_list = list(json.loads(event[2])['operations'])
        if func_name in operations_list:
            updated_op = {"operations": operations_list}
            updated_op["operations"].remove(func_name)
            c.execute("UPDATE event_types SET operations = ? WHERE id = ?", (json.dumps(updated_op), event[0]))
            conn.commit()
        conn.close()
        return {"message": f"Operation {func_name} removed from event type {event_type}."}

    @staticmethod
    def del_event(event_type: str) -> dict:
        conn = sqlite3.connect("py_usher.db")
        c = conn.cursor()
        c.execute("DELETE FROM event_types WHERE event_name = ?", (event_type,))
        conn.commit()
        conn.close()
        return {"message": f"{event_type} has been deleted from the db."}


if __name__ == "__main__":

    def test():
        return "lol"

    db = DBHandler()
    db.insert_new("test_event", "trythis")
    db.insert_new("test_event", "nowthis")
    print("fetched event - " + str(db.fetch_event("test_event")))
    db.del_operation("test_event", "nowthis")
    # db.del_event("test_event")
    print("fetched event - " + str(db.fetch_event("test_event")))
