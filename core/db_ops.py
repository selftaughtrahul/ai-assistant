import sqlite3

def get_order_details(order_id: str):
    try:
        conn = sqlite3.connect("company_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id.upper(),))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            return {
                "order_id": record[0],
                "customer_name": record[1],
                "status": record[2],
                "item_name": record[3],
                "amount": record[4]
            }
        return None
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def get_demand_details(demand_id: str):
    try:
        conn = sqlite3.connect("company_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demands WHERE demand_id = ?", (demand_id.upper(),))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            return {
                "demand_id": record[0],
                "requestor_name": record[1],
                "department": record[2],
                "status": record[3],
                "priority": record[4],
                "estimated_budget": record[5]
            }
        return None
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def get_project_details(project_id: str):
    try:
        conn = sqlite3.connect("company_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE project_id = ?", (project_id.upper(),))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            return {
                "project_id": record[0],
                "project_name": record[1],
                "demand_id": record[2],
                "manager": record[3],
                "status": record[4],
                "start_date": record[5]
            }
        return None
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def get_resource_details(resource_id: str):
    try:
        conn = sqlite3.connect("company_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resources WHERE resource_id = ?", (resource_id.upper(),))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            return {
                "resource_id": record[0],
                "resource_name": record[1],
                "role": record[2],
                "availability_status": record[3]
            }
        return None
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def update_order_status(order_id: str, new_status: str):
    try:
        conn = sqlite3.connect("company_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status.capitalize(), order_id.upper()))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def update_demand_status(demand_id: str, new_status: str):
    try:
        conn = sqlite3.connect("company_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE demands SET status = ? WHERE demand_id = ?", (new_status.title(), demand_id.upper()))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    except Exception as e:
        print(f"DB Error: {e}")
        return False
