from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any, Dict
import mysql.connector
from app.config import Config
from app.services.guardrails import validate_query
from app.services.sql_generator import generate_sql

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    sql: str
    result: List[Dict[str, Any]]
    highlight_ids: List[str]  # New field for highlighted nodes

def extract_highlight_ids(result: List[Dict], query_text: str) -> List[str]:
    """
    Extract IDs from SQL result for highlighting
    """
    highlight_ids = []
    
    # Define ID field mappings for different entity types
    id_mappings = {
        'customer': ['customer_id', 'sold_to_party', 'customer'],
        'order': ['order_id', 'sales_order'],
        'delivery': ['delivery_id', 'delivery_document'],
        'invoice': ['invoice_id', 'billing_document'],
        'payment': ['payment_id', 'accounting_document']
    }
    
    for row in result:
        # Check each possible ID field
        for entity_type, fields in id_mappings.items():
            for field in fields:
                if field in row and row[field]:
                    # Create node ID format matching frontend
                    node_id = f"{entity_type}_{row[field]}"
                    highlight_ids.append(node_id)
                    
        # Also check for IDs in any field with 'id' in the name
        for key, value in row.items():
            if 'id' in key.lower() and value:
                # Try to determine entity type from field name
                for entity_type in id_mappings.keys():
                    if entity_type in key.lower():
                        node_id = f"{entity_type}_{value}"
                        highlight_ids.append(node_id)
                        break
    
    # Remove duplicates
    return list(set(highlight_ids))

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process natural language query and return results with highlight IDs
    """
    try:
        # 1. Validate query is within domain
        is_valid, error_msg = validate_query(request.query)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # 2. Generate SQL from natural language
        sql_query = generate_sql(request.query)
        
        # 3. Execute SQL
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # 4. Extract IDs for highlighting
        highlight_ids = extract_highlight_ids(result, request.query)
        
        # 5. Return response
        return QueryResponse(
            sql=sql_query,
            result=result,
            highlight_ids=highlight_ids
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))