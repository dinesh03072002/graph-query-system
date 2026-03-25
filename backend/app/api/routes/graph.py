from fastapi import APIRouter
from app.graph.builder import get_graph

router = APIRouter()

@router.get("/graph")
def get_graph_data():
    return get_graph()