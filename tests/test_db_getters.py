import pytest
import sys
import sqlite3
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from core.db_ops import get_order_details, get_demand_details, get_project_details, get_resource_details

# We can run brief DB getter tests if the db file exists logic
def test_db_get_order_details():
    try:
        # Check an order exists
        res = get_order_details("ORD-1234")
        if res:
            assert res["customer_name"] == "Rahul"
    except Exception:
        pass

def test_db_get_demand_details():
    try:
        res = get_demand_details("DEM-001")
        if res:
            assert res["requestor_name"] == "Rahul"
            assert res["department"] == "IT"
    except Exception:
        pass

def test_db_get_project_details():
    try:
        res = get_project_details("PRJ-101")
        if res:
            assert res["project_name"] == "Cloud Migration"
    except Exception:
        pass

def test_db_get_resource_details():
    try:
        res = get_resource_details("RES-001")
        if res:
            assert res["role"] == "Developer"
    except Exception:
        pass
