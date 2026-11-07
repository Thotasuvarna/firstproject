"""
Pydantic schemas for Network Graph visualizer (nodes, edges, clusters).
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    node_type: str  # 'reviewer' or 'product'
    risk_score: float  # 0 to 100
    group: Optional[str] = "Normal"
    metadata: Optional[Dict[str, Any]] = None


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    weight: float = 1.0
    edge_type: str = "reviewed"
    metadata: Optional[Dict[str, Any]] = None


class GraphDataResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    total_nodes: int
    total_edges: int
    detected_clusters_count: int
