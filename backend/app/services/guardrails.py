import re

# Domain-specific keywords
ALLOWED_TOPICS = [
    'customer', 'order', 'delivery', 'invoice', 'payment',
    'sales', 'billing', 'shipping', 'amount', 'total',
    'status', 'date', 'flow', 'track', 'incomplete', 'broken'
]

# Blocked topics
BLOCKED_TOPICS = [
    'weather', 'news', 'sports', 'movie', 'music', 'game',
    'politics', 'stock', 'crypto', 'bitcoin', 'write', 
    'poem', 'story', 'essay', 'email', 'letter', 'hello', 'hi'
]

def validate_query(query: str):
    """
    Validate if query is within the business domain
    """
    query_lower = query.lower()
    
    # Check if query is just greeting
    if query_lower.strip() in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']:
        return True, ""  # Allow greetings, will get default response
    
    # Check for blocked topics
    for blocked in BLOCKED_TOPICS:
        if blocked in query_lower:
            return False, f"This system only answers questions about business data (orders, customers, invoices, payments, deliveries). Please ask about the dataset."
    
    # Allow if contains allowed topics
    has_allowed = any(topic in query_lower for topic in ALLOWED_TOPICS)
    
    # Check if it's a number query (like "customer 123")
    has_number = bool(re.search(r'\d+', query_lower))
    
    if not has_allowed and not has_number:
        return False, "Please ask questions related to customers, orders, deliveries, invoices, or payments."
    
    return True, ""