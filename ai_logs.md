# AI CODING SESSION LOG 

##  Overview
AI tools were actively used throughout development to speed up implementation, debug issues, and improve code quality.

##  Tools Used

- ChatGPT
- DeepSeek


## Workflow

### 1. Project Setup
Used AI to:
- Decide tech stack (FastAPI + React + MySQL + Cytoscape)
- Design project structure

Prompt:
"Suggest a full-stack architecture for a graph-based query system using AI"


### 2. Database Design
Used AI to:
- Simplify SAP dataset
- Create relational schema

Prompt:
"Convert SAP dataset into simplified MySQL schema with customers, orders, invoices, payments"


### 3. Data Loading
Used AI to:
- Map JSONL data to SQL tables
- Write loading scripts

Prompt:
"Map JSON fields to MySQL columns and generate insert logic"


### 4. Graph Construction
Used AI to:
- Build graph nodes and edges
- Optimize structure

Prompt:
"Generate graph structure from relational database for Cytoscape visualization"


### 5. Frontend Development
Used AI to:
- Implement Cytoscape graph
- Improve UI layout and styling

Prompt:
"Improve Cytoscape graph layout, avoid overlap, and color nodes by type"


### 6. AI Query Integration
Used AI to:
- Convert natural language to SQL
- Improve prompt engineering

Prompt:
"Convert natural language queries into SQL using database schema"


### 7. Debugging & Iteration
Used AI to:
- Fix SQL errors
- Handle null relationships
- Resolve API issues

Prompt:
"Fix SQL generation issues and avoid invalid queries like SELECT 1"


### 8. Graph Highlighting
Used AI to:
- Extract IDs from query results
- Highlight nodes dynamically

Prompt:
"Extract IDs from SQL results and highlight corresponding graph nodes"


##  Key Learnings

- Importance of prompt engineering
- Handling AI model failures
- Designing fallback mechanisms
- Debugging full-stack applications



## Challenges & Solutions

### Issue: Invalid SQL (SELECT 1)
Solution:
- Improved prompts with examples and constraints

### Issue: API Model Errors
Solution:
- Adjusted model naming and added fallback logic

### Issue: Graph Clutter
Solution:
- Optimized layout and filtered nodes

