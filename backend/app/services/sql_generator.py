import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sql(natural_language_query: str) -> str:
    """
    Generate SQL from natural language using pattern matching
    """
    query_lower = natural_language_query.lower().strip()
    
    logger.info(f"Generating SQL for: {query_lower}")
    
    # ========== INVOICE PAYMENT QUERIES ==========
    
    # Pattern: Show payments for invoice X
    invoice_payment_pattern = r'(?:show|list|display|get|find)\s+(?:payments?|payment details?)\s+(?:for|of|from)\s+invoice\s+(\d+)'
    match = re.search(invoice_payment_pattern, query_lower)
    if match:
        invoice_id = match.group(1)
        return f"""
        SELECT 
            p.payment_id,
            p.accounting_doc,
            p.customer_id,
            p.payment_date,
            p.amount,
            i.invoice_id,
            i.total_amount as invoice_amount
        FROM payments p
        JOIN invoices i ON p.accounting_doc = i.accounting_doc
        WHERE i.invoice_id = '{invoice_id}'
        ORDER BY p.payment_date DESC
        """
    
    # Pattern: Check if invoice is paid
    invoice_paid_pattern = r'(?:is|check)\s+invoice\s+(\d+)\s+(?:paid|has payment|payment status)'
    match = re.search(invoice_paid_pattern, query_lower)
    if match:
        invoice_id = match.group(1)
        return f"""
        SELECT 
            i.invoice_id,
            i.total_amount,
            CASE WHEN p.payment_id IS NOT NULL THEN 'Paid' ELSE 'Not Paid' END as payment_status,
            SUM(p.amount) as total_paid
        FROM invoices i
        LEFT JOIN payments p ON i.accounting_doc = p.accounting_doc
        WHERE i.invoice_id = '{invoice_id}'
        GROUP BY i.invoice_id, i.total_amount, p.payment_id
        """
    
    # Pattern: Payment amount for invoice X
    invoice_payment_amount = r'(?:payment amount|how much paid|total payment)\s+(?:for|of)\s+invoice\s+(\d+)'
    match = re.search(invoice_payment_amount, query_lower)
    if match:
        invoice_id = match.group(1)
        return f"""
        SELECT 
            i.invoice_id,
            i.total_amount,
            SUM(p.amount) as total_paid,
            CASE 
                WHEN SUM(p.amount) >= i.total_amount THEN 'Fully Paid'
                WHEN SUM(p.amount) > 0 THEN 'Partially Paid'
                ELSE 'Not Paid'
            END as payment_status
        FROM invoices i
        LEFT JOIN payments p ON i.accounting_doc = p.accounting_doc
        WHERE i.invoice_id = '{invoice_id}'
        GROUP BY i.invoice_id, i.total_amount
        """
    
    # ========== CUSTOMER PAYMENT QUERIES ==========
    
    # Pattern: Total payment amount for customer X
    customer_payment_pattern = r'(?:total payment|payment total|total paid)\s+(?:amount\s+)?(?:for|by|from)\s+customer\s+(\d+)'
    match = re.search(customer_payment_pattern, query_lower)
    if match:
        customer_id = match.group(1)
        return f"""
        SELECT 
            c.customer_id,
            c.customer_name,
            COUNT(p.payment_id) as payment_count,
            SUM(p.amount) as total_paid_amount
        FROM customers c
        LEFT JOIN payments p ON c.customer_id = p.customer_id
        WHERE c.customer_id = '{customer_id}'
        GROUP BY c.customer_id, c.customer_name
        """
    
    # Pattern: Show payments for customer X
    customer_payments_pattern = r'(?:show|list|display)\s+(?:payments?|payment history)\s+(?:for|of|from)\s+customer\s+(\d+)'
    match = re.search(customer_payments_pattern, query_lower)
    if match:
        customer_id = match.group(1)
        return f"""
        SELECT 
            p.payment_id,
            p.accounting_doc,
            p.payment_date,
            p.amount,
            i.invoice_id
        FROM payments p
        JOIN customers c ON p.customer_id = c.customer_id
        LEFT JOIN invoices i ON p.accounting_doc = i.accounting_doc
        WHERE c.customer_id = '{customer_id}'
        ORDER BY p.payment_date DESC
        LIMIT 20
        """
    
    # ========== ORDER QUERIES ==========
    
    # Pattern: Show orders for customer X
    orders_pattern = r'(?:show|list|display)\s+(?:orders?)\s+(?:for|of|from)\s+customer\s+(\d+)'
    match = re.search(orders_pattern, query_lower)
    if match:
        customer_id = match.group(1)
        return f"""
        SELECT 
            o.order_id,
            o.order_date,
            o.total_amount,
            o.status,
            c.customer_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.customer_id = '{customer_id}'
        ORDER BY o.order_date DESC
        LIMIT 20
        """
    
    # ========== INVOICE QUERIES ==========
    
    # Pattern: Show top invoices
    if 'top' in query_lower and 'invoice' in query_lower and ('amount' in query_lower or 'highest' in query_lower):
        limit = 5
        if '5' in query_lower:
            limit = 5
        elif '10' in query_lower:
            limit = 10
        return f"""
        SELECT invoice_id, total_amount, is_cancelled, accounting_doc
        FROM invoices
        WHERE is_cancelled = false
        ORDER BY total_amount DESC
        LIMIT {limit}
        """
    
    # Pattern: Show all invoices
    if query_lower in ['show invoices', 'list invoices', 'display invoices', 'invoices']:
        return "SELECT * FROM invoices LIMIT 10"
    
    # Pattern: Show specific invoice
    invoice_pattern = r'(?:show|list|display)\s+invoice\s+(\d+)'
    match = re.search(invoice_pattern, query_lower)
    if match:
        invoice_id = match.group(1)
        return f"""
        SELECT 
            i.*,
            CASE WHEN p.payment_id IS NOT NULL THEN 'Paid' ELSE 'Unpaid' END as payment_status,
            SUM(p.amount) as paid_amount
        FROM invoices i
        LEFT JOIN payments p ON i.accounting_doc = p.accounting_doc
        WHERE i.invoice_id = '{invoice_id}'
        GROUP BY i.invoice_id
        """
    
    # ========== PAYMENT QUERIES ==========
    
    # Pattern: Show all payments
    if query_lower in ['show payments', 'list payments', 'display payments', 'payments']:
        return "SELECT * FROM payments LIMIT 10"
    
    # ========== CUSTOMER QUERIES ==========
    
    # Pattern: Show all customers
    if query_lower in ['show customers', 'list customers', 'display customers', 'customers']:
        return "SELECT * FROM customers LIMIT 10"
    
    # Pattern: Show specific customer
    customer_pattern = r'(?:show|list|display)\s+customer\s+(\d+)'
    match = re.search(customer_pattern, query_lower)
    if match:
        customer_id = match.group(1)
        return f"""
        SELECT 
            c.*,
            COUNT(DISTINCT o.order_id) as order_count,
            COUNT(DISTINCT i.invoice_id) as invoice_count,
            SUM(p.amount) as total_paid
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN invoices i ON o.order_id = i.order_id
        LEFT JOIN payments p ON c.customer_id = p.customer_id
        WHERE c.customer_id = '{customer_id}'
        GROUP BY c.customer_id
        """
    
    # ========== FLOW ANALYSIS QUERIES ==========
    
    # Pattern: Trace full flow
    flow_pattern = r'(?:trace|show|get)\s+(?:full\s+)?flow\s+(?:for|of)\s+(?:order|invoice)\s+(\d+)'
    match = re.search(flow_pattern, query_lower)
    if match:
        doc_id = match.group(1)
        return f"""
        SELECT 
            c.customer_name,
            o.order_id,
            o.total_amount as order_amount,
            d.delivery_id,
            d.delivery_date,
            i.invoice_id,
            i.total_amount as invoice_amount,
            p.payment_id,
            p.amount as payment_amount,
            p.payment_date
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN deliveries d ON o.order_id = d.order_id
        LEFT JOIN invoices i ON o.order_id = i.order_id
        LEFT JOIN payments p ON i.accounting_doc = p.accounting_doc
        WHERE o.order_id = '{doc_id}' OR i.invoice_id = '{doc_id}'
        """
    
    # Pattern: Broken flows
    if 'broken' in query_lower or 'incomplete' in query_lower:
        if 'delivered' in query_lower and 'invoiced' in query_lower:
            return """
            SELECT 
                o.order_id,
                CASE WHEN d.delivery_id IS NOT NULL THEN 'Yes' ELSE 'No' END as has_delivery,
                CASE WHEN i.invoice_id IS NOT NULL THEN 'Yes' ELSE 'No' END as has_invoice
            FROM orders o
            LEFT JOIN deliveries d ON o.order_id = d.order_id
            LEFT JOIN invoices i ON o.order_id = i.order_id
            WHERE (d.delivery_id IS NOT NULL AND i.invoice_id IS NULL)
               OR (d.delivery_id IS NULL AND i.invoice_id IS NOT NULL)
            LIMIT 10
            """
        else:
            return """
            SELECT 
                o.order_id,
                CASE WHEN d.delivery_id IS NULL THEN 'Missing Delivery' 
                     WHEN i.invoice_id IS NULL THEN 'Missing Invoice' 
                     ELSE 'Complete' END as flow_status
            FROM orders o
            LEFT JOIN deliveries d ON o.order_id = d.order_id
            LEFT JOIN invoices i ON o.order_id = i.order_id
            WHERE d.delivery_id IS NULL OR i.invoice_id IS NULL
            LIMIT 10
            """
    
    # ========== AGGREGATION QUERIES ==========
    
    # Pattern: Total revenue
    if 'total revenue' in query_lower or 'total sales' in query_lower:
        return "SELECT SUM(total_amount) as total_revenue FROM orders"
    
    # Pattern: Average order value
    if 'average order' in query_lower:
        return "SELECT AVG(total_amount) as avg_order_value FROM orders"
    
    # Pattern: Total payments
    if 'total payments' in query_lower:
        return "SELECT SUM(amount) as total_payments FROM payments"
    
    # ========== DEFAULT ==========
    
    # If no pattern matches, return a helpful response query
    return """
    SELECT 'Please try one of these queries:' as message
    UNION ALL SELECT '- Show payments for invoice 90504204'
    UNION ALL SELECT '- Show orders for customer 310000108'
    UNION ALL SELECT '- Total payment amount for customer 320000083'
    UNION ALL SELECT '- List all invoices'
    UNION ALL SELECT '- Show top 5 invoices by amount'
    """