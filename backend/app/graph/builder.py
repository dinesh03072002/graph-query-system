import mysql.connector

def get_graph():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dineshyuvi@12",
        database="graph_db"
    )

    cursor = conn.cursor(dictionary=True)

    nodes = []
    edges = []

    # -------- CUSTOMERS --------
    cursor.execute("SELECT customer_id, customer_name FROM customers LIMIT 50")
    for c in cursor.fetchall():
        nodes.append({
            "id": f"customer_{c['customer_id']}",
            "label": c["customer_name"]
        })

    # -------- ORDERS --------
    cursor.execute("SELECT order_id, customer_id FROM orders LIMIT 50")
    for o in cursor.fetchall():
        nodes.append({
            "id": f"order_{o['order_id']}",
            "label": f"Order {o['order_id']}"
        })

        edges.append({
            "source": f"customer_{o['customer_id']}",
            "target": f"order_{o['order_id']}",
            "label": "placed"
        })

    # -------- INVOICES --------
    cursor.execute("SELECT invoice_id, order_id FROM invoices LIMIT 50")
    for i in cursor.fetchall():
        nodes.append({
            "id": f"invoice_{i['invoice_id']}",
            "label": f"Invoice {i['invoice_id']}"
        })

        if i['order_id']:
            edges.append({
                "source": f"order_{i['order_id']}",
                 "target": f"invoice_{i['invoice_id']}",
                "label": "billed"
            })

    # -------- PAYMENTS --------
    cursor.execute("SELECT payment_id, invoice_id FROM payments LIMIT 50")
    for p in cursor.fetchall():
        nodes.append({
            "id": f"payment_{p['payment_id']}",
            "label": f"Payment {p['payment_id']}"
        })

        if p['invoice_id']:
            edges.append({
                "source": f"invoice_{p['invoice_id']}",
                "target": f"payment_{p['payment_id']}",
                "label": "paid"
            })

    conn.close()

    return {"nodes": nodes, "edges": edges}