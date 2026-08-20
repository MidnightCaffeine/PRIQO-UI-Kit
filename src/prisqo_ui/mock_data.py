"""Realistic mock ERP data — for showcase and lookup demos only.

No database, no API. Nothing in this module performs business logic.
"""
from __future__ import annotations

ITEMS = [
    {"sku": "BEV-001", "name": "Coca-Cola 1L", "category": "Beverage", "stock": 120, "uom": "PCS", "price": 75.00, "status": "In Stock"},
    {"sku": "BEV-002", "name": "Pepsi 1L", "category": "Beverage", "stock": 85, "uom": "PCS", "price": 70.00, "status": "In Stock"},
    {"sku": "GRO-001", "name": "Nescafe Classic", "category": "Grocery", "stock": 12, "uom": "JAR", "price": 150.00, "status": "Low Stock"},
    {"sku": "GRO-002", "name": "Lucky Me Pancit Canton", "category": "Grocery", "stock": 300, "uom": "PACK", "price": 15.00, "status": "In Stock"},
    {"sku": "DAI-001", "name": "Bear Brand Milk", "category": "Dairy", "stock": 0, "uom": "CAN", "price": 55.00, "status": "Out of Stock"},
]

CUSTOMERS = [
    {"code": "CUST-000", "name": "Walk-in Customer", "type": "Retail", "terms": "Cash"},
    {"code": "CUST-001", "name": "ABC Trading", "type": "Wholesale", "terms": "Net 30"},
    {"code": "CUST-002", "name": "Juan Dela Cruz", "type": "Retail", "terms": "Cash"},
    {"code": "CUST-003", "name": "XYZ Corporation", "type": "Corporate", "terms": "Net 60"},
]

VENDORS = [
    {"code": "VEND-001", "name": "ABC Distributors", "category": "Beverage", "terms": "Net 30"},
    {"code": "VEND-002", "name": "Metro Supply", "category": "Grocery", "terms": "Net 15"},
    {"code": "VEND-003", "name": "Global Foods Inc.", "category": "Dairy", "terms": "Net 45"},
]

EMPLOYEES = [
    {"id": "EMP-001", "name": "Maria Santos", "department": "Sales", "role": "Cashier"},
    {"id": "EMP-002", "name": "Pedro Reyes", "department": "Warehouse", "role": "Inventory Clerk"},
    {"id": "EMP-003", "name": "Ana Lim", "department": "Accounting", "role": "Bookkeeper"},
]

LOCATIONS = [
    {"code": "LOC-001", "name": "Main Warehouse", "city": "Quezon City"},
    {"code": "LOC-002", "name": "Branch 1 - Makati", "city": "Makati"},
    {"code": "LOC-003", "name": "Branch 2 - Cebu", "city": "Cebu City"},
]
