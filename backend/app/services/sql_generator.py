import google.generativeai as genai
from app.config import Config
import re

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)

# List available models to verify
try:
    models = genai.list_models()
    available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
    print("Available models:", available_models)
except Exception as e:
    print(f"Error listing models: {e}")

def generate_sql(natural_language_query: str) -> str:
    """
    Generate SQL from natural language using Gemini
    """
    try:
        # Get the model
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Define the system prompt
        prompt = f"""
You are an expert SQL assistant for a business database.

Database Schema:
- customers (customer_id VARCHAR, customer_name VARCHAR, created_date DATE)
- orders (order_id VARCHAR, customer_id VARCHAR, order_date DATE, total_amount DECIMAL, status VARCHAR)
- deliveries (delivery_id VARCHAR, order_id VARCHAR, delivery_date DATE, status VARCHAR)
- invoices (invoice_id VARCHAR, order_id VARCHAR, invoice_date DATE, total_amount DECIMAL, is_cancelled BOOLEAN, accounting_doc VARCHAR)
- payments (payment_id INT, accounting_doc VARCHAR, customer_id VARCHAR, payment_date DATE, amount DECIMAL)

Important:
- IDs are stored as VARCHAR
- Use customer_id to join customers and orders
- Use order_id to join orders with deliveries and invoices
- Use accounting_doc to join invoices with payments

Convert this question to SQL: "{natural_language_query}"

Return ONLY the SQL query, no explanation, no markdown formatting.
"""

        # Generate SQL
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        
        # Remove markdown code blocks if present
        sql_query = re.sub(r'```sql\n?', '', sql_query)
        sql_query = re.sub(r'```\n?', '', sql_query)
        
        # Basic validation
        if not sql_query.lower().startswith('select'):
            # If no SELECT, try to add a default
            sql_query = f"SELECT * FROM orders LIMIT 10"
        
        return sql_query
        
    except Exception as e:
        print(f"Error generating SQL: {e}")
        # Fallback SQL based on keywords
        return fallback_sql_generator(natural_language_query)

def fallback_sql_generator(query: str) -> str:
    """
    Simple keyword-based SQL generator as fallback
    """
    query_lower = query.lower()
    
    # Customer queries
    if "customer" in query_lower:
        if "total payment" in query_lower or "payment amount" in query_lower:
            # Extract customer ID if present
            import re
            customer_match = re.search(r'customer\s+(\d+)', query_lower)
            if customer_match:
                customer_id = customer_match.group(1)
                return f"""
                SELECT c.customer_name, SUM(p.amount) as total_payments
                FROM customers c
                JOIN payments p ON c.customer_id = p.customer_id
                WHERE c.customer_id = '{customer_id}'
                GROUP BY c.customer_id, c.customer_name
                """
            else:
                return """
                SELECT c.customer_name, SUM(p.amount) as total_payments
                FROM customers c
                JOIN payments p ON c.customer_id = p.customer_id
                GROUP BY c.customer_id, c.customer_name
                ORDER BY total_payments DESC
                LIMIT 10
                """
    
    # Orders queries
    elif "order" in query_lower:
        if "customer" in query_lower:
            return """
            SELECT o.order_id, c.customer_name, o.total_amount, o.status
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            LIMIT 10
            """
        else:
            return "SELECT * FROM orders LIMIT 10"
    
    # Invoices queries
    elif "invoice" in query_lower:
        if "highest" in query_lower or "top" in query_lower:
            return """
            SELECT invoice_id, total_amount, is_cancelled
            FROM invoices
            ORDER BY total_amount DESC
            LIMIT 5
            """
        return "SELECT * FROM invoices LIMIT 10"
    
    # Payments queries
    elif "payment" in query_lower:
        return """
        SELECT p.*, c.customer_name
        FROM payments p
        JOIN customers c ON p.customer_id = c.customer_id
        ORDER BY p.payment_date DESC
        LIMIT 10
        """
    
    # Default
    return "SELECT * FROM orders LIMIT 10"