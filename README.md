# Graph Query System with AI Integration

## Overview
This project is a full-stack Graph Query System that allows users to:

- Visualize business data as a graph
- Query data using natural language
- Convert queries into SQL using AI
- Highlight relevant nodes in the graph dynamically

The system represents a simplified Order-to-Cash (O2C) business flow:

Customer → Order → Invoice → Payment

---

## Features

- Graph Visualization using Cytoscape.js
- Natural Language Query using AI (Gemini / fallback logic)
- SQL Generation from user queries
- Dynamic Node Highlighting based on query results
- FastAPI backend with MySQL database
- Chat-based UI for querying

---

## Tech Stack

### Frontend
- React.js
- Cytoscape.js

### Backend
- FastAPI
- MySQL
- Google Generative AI (Gemini API)


---

## Setup Instructions

### 1. Backend Setup

cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

**create .env:**

DB_HOST=localhost

DB_USER=root

DB_PASSWORD=your_password

DB_NAME=graph_db

GEMINI_API_KEY=your_api_key

**Run Backend:**

uvicorn app.main:app --reload

### 2. Frontend Setup

cd frontend

npm install

npm run dev
