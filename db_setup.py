import sqlite3
import argparse
import random

def setup_mock_db(db_name="company_data.db"):
    # Connect (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop existing to ensure fresh start
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS demands')
    cursor.execute('DROP TABLE IF EXISTS projects')
    cursor.execute('DROP TABLE IF EXISTS resources')

    # Create an Orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            status TEXT,
            item_name TEXT,
            amount REAL
        )
    ''')
    
    # Insert some dummy orders
    mock_orders = [
        ('ORD-1234', 'Rahul', 'Shipped', 'Wireless Mouse', 25.99),
        ('ORD-5678', 'Anjali', 'Processing', 'Mechanical Keyboard', 89.50),
        ('ORD-9101', 'Vikram', 'Delivered', 'Gaming Monitor', 249.00),
        ('ORD-1122', 'Ria', 'Cancelled', 'USB-C Cable', 12.99),
        ('ORD-9999', 'Sara', 'Pending', 'Laptop Stand', 45.00)
    ]
    
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', mock_orders)
    
    # Create Demands table
    cursor.execute('''
        CREATE TABLE demands (
            demand_id TEXT PRIMARY KEY,
            requestor_name TEXT,
            department TEXT,
            status TEXT,
            priority TEXT,
            estimated_budget REAL
        )
    ''')
    
    mock_demands = [
        ('DEM-001', 'Rahul', 'IT', 'Approved', 'High', 50000.00),
        ('DEM-002', 'Anjali', 'HR', 'Under Review', 'Medium', 15000.00),
        ('DEM-003', 'Vikram', 'Finance', 'Rejected', 'Low', 5000.00),
        ('DEM-004', 'Ria', 'Marketing', 'Draft', 'High', 25000.00),
        ('DEM-005', 'Sara', 'Operations', 'Approved', 'Critical', 100000.00)
    ]
    cursor.executemany('INSERT INTO demands VALUES (?, ?, ?, ?, ?, ?)', mock_demands)

    # Create Projects table
    cursor.execute('''
        CREATE TABLE projects (
            project_id TEXT PRIMARY KEY,
            project_name TEXT,
            demand_id TEXT,
            manager TEXT,
            status TEXT,
            start_date TEXT
        )
    ''')
    
    mock_projects = [
        ('PRJ-101', 'Cloud Migration', 'DEM-001', 'John Doe', 'In Progress', '2023-01-15'),
        ('PRJ-102', 'ERP Upgrade', 'DEM-005', 'Jane Smith', 'Planning', '2023-03-01'),
        ('PRJ-103', 'Marketing Portal', 'DEM-004', 'Alice Brown', 'Not Started', '2023-06-10')
    ]
    cursor.executemany('INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)', mock_projects)

    # Create Resources table
    cursor.execute('''
        CREATE TABLE resources (
            resource_id TEXT PRIMARY KEY,
            resource_name TEXT,
            role TEXT,
            availability_status TEXT
        )
    ''')
    
    mock_resources = [
        ('RES-001', 'Bob Martin', 'Developer', 'Available'),
        ('RES-002', 'Eve Davis', 'Designer', 'Busy'),
        ('RES-003', 'Charlie Lee', 'Project Manager', 'Available')
    ]
    cursor.executemany('INSERT INTO resources VALUES (?, ?, ?, ?)', mock_resources)
    
    conn.commit()
    conn.close()
    print(f"✅ Mock Database created successfully: {db_name}")

if __name__ == "__main__":
    setup_mock_db()
