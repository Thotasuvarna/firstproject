"""
Graph Network API Endpoints.
Serves nodes, edges, and detected collusion rings for interactive visualization.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.models.reviewer import Reviewer
from app.models.review import Review
from app.models.analysis import ReviewAnalysis
from app.models.cluster import CollusionCluster, ClusterMembership
from app.schemas.graph import GraphDataResponse
from app.services.graph_service import graph_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/graph", tags=["Network Analysis"])


@router.get("/network", response_model=GraphDataResponse)
def get_network_graph(
    min_shared: int = Query(1, ge=1, description="Minimum shared products for co-review edge"),
    limit: int = Query(250, ge=10, le=1000),
    db: Session = Depends(get_db)
):
    """
    Constructs and returns bipartite Reviewer-Product graph data
    with nodes and edges formatted for React graph visualizers.
    """
    # Fetch reviews
    reviews = (
        db.query(Review, Reviewer, Product, ReviewAnalysis)
        .join(Reviewer, Review.reviewer_id == Reviewer.id)
        .join(Product, Review.product_id == Product.id)
        .outerjoin(ReviewAnalysis, Review.id == ReviewAnalysis.review_id)
        .order_by(Review.id.desc())
        .limit(limit)
        .all()
    )

    records = []
    for rev, reviewer, prod, analysis in reviews:
        records.append({
            "reviewer_id": rev.reviewer_id,
            "reviewer_alias": reviewer.display_alias,
            "reviewer_anomaly_score": reviewer.anomaly_score,
            "product_id": rev.product_id,
            "product_title": prod.title,
            "product_trust_score": prod.product_trust_score,
            "rating": rev.rating,
            "suspicion_score": analysis.composite_suspicion_score if analysis else 0.0
        })

    # Build bipartite graph
    B = graph_service.build_bipartite_graph(records)

    # Project co-review graph and mine clusters
    co_graph = graph_service.project_co_review_graph(B, min_shared_products=min_shared)
    clusters = graph_service.detect_collusion_clusters(co_graph)

    # Sync detected clusters into database for persistent auditing
    for c in clusters:
        db_cluster = db.query(CollusionCluster).filter(CollusionCluster.cluster_name == c["cluster_name"]).first()
        if not db_cluster:
            db_cluster = CollusionCluster(
                cluster_name=c["cluster_name"],
                collusion_density=c["density"],
                member_count=c["member_count"],
                co_reviewed_products_count=int(c["avg_co_reviews"]),
                status="DETECTED"
            )
            db.add(db_cluster)
            db.flush()

            for m in c["members"]:
                db.add(ClusterMembership(
                    cluster_id=db_cluster.id,
                    reviewer_id=m["raw_reviewer_id"],
                    centrality_score=m["centrality"]
                ))
    db.commit()

    # Export graph payload
    return graph_service.export_graph_for_visualization(B, clusters)


@router.get("/clusters")
def list_collusion_clusters(db: Session = Depends(get_db)):
    """Retrieves all detected collusion rings for human inspection."""
    clusters = db.query(CollusionCluster).order_by(CollusionCluster.collusion_density.desc()).all()
    out = []
    for c in clusters:
        members = [
            {
                "reviewer_id": m.reviewer_id,
                "alias": m.reviewer.display_alias,
                "centrality": m.centrality_score,
                "total_reviews": m.reviewer.total_reviews_count
            }
            for m in c.memberships
        ]
        out.append({
            "id": c.id,
            "cluster_name": c.cluster_name,
            "density": c.collusion_density,
            "member_count": c.member_count,
            "status": c.status,
            "detected_at": c.detected_at,
            "members": members
        })
    return out
