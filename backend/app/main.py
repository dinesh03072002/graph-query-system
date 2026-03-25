from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config
from app.api.routes.graph import router as graph_router
from app.api.routes.query import router as query_router





app = FastAPI(title="Graph Query System", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Graph Query System API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(graph_router)
app.include_router(query_router)