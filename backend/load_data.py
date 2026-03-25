import json
import mysql.connector
from datetime import datetime

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Dineshyuvi@12',
    'database': 'graph_db'
}

def parse_date(date_str):
    if not date_str:
        return None
    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()

# Connect
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Load customers
print("Loading customers...")
with open('data/business_partners.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data.get('customer'):
            cursor.execute("""
                INSERT INTO customers (customer_id, customer_name, created_date)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE customer_name = VALUES(customer_name)
            """, (
                data['customer'],
                data.get('organizationBpName1', data.get('businessPartnerName', 'Unknown')),
                parse_date(data.get('creationDate'))
            ))
conn.commit()
print(f"✓ Loaded customers")

# Load orders
print("Loading orders...")
with open('data/sales_order_headers.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data.get('salesOrder') and data.get('soldToParty'):
            cursor.execute("""
                INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE total_amount = VALUES(total_amount)
            """, (
                data['salesOrder'],
                data['soldToParty'],
                parse_date(data.get('creationDate')),
                float(data.get('totalNetAmount', 0)),
                data.get('overallDeliveryStatus', '')
            ))
conn.commit()
print(f"✓ Loaded orders")

# Load deliveries
print("Loading deliveries...")
with open("data/outbound_delivery_headers.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        cursor.execute("""
    INSERT INTO deliveries (delivery_id, delivery_date, status)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE status = VALUES(status)
""", (
    data.get("deliveryDocument"),
    data.get("creationDate")[:10] if data.get("creationDate") else None,
    data.get("overallGoodsMovementStatus")
))
conn.commit()
print(f"✓ Loaded deliveries")

# Load invoices
print("Loading invoices...")
with open('data/billing_document_headers.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data.get('billingDocument'):
            cursor.execute("""
                INSERT INTO invoices (invoice_id, order_id, invoice_date, total_amount, is_cancelled, accounting_doc)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE total_amount = VALUES(total_amount)
            """, (
                data['billingDocument'],
                None,  # No order link available
                parse_date(data.get('billingDocumentDate')),
                float(data.get('totalNetAmount', 0)),
                data.get('billingDocumentIsCancelled', False),
                data.get('accountingDocument')
            ))
conn.commit()
print(f"✓ Loaded invoices")

# Load payments
print("Loading payments...")
with open('data/payments_accounts_receivable.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data.get('accountingDocument') and data.get('customer'):
            cursor.execute("""
                INSERT INTO payments (accounting_doc, customer_id, payment_date, amount)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE amount = VALUES(amount)
            """, (
                data['accountingDocument'],
                data['customer'],
                parse_date(data.get('clearingDate')),
                float(data.get('amountInTransactionCurrency', 0))
            ))
conn.commit()
print(f"✓ Loaded payments")

# Show summary
cursor.execute("SELECT COUNT(*) FROM customers")
print(f"\nTotal customers: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM orders")
print(f"Total orders: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM deliveries")
print(f"Total deliveries: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM invoices")
print(f"Total invoices: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM payments")
print(f"Total payments: {cursor.fetchone()[0]}")

cursor.close()
conn.close()
print("\n✓ Done!")