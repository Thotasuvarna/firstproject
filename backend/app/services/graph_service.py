"""
Graph Network Analysis Service (NetworkX).
Models bipartite Reviewer-Product graphs, computes co-review projections,
and identifies coordinated collusion rings and dense subgraphs.
"""
from typing import List, Dict, Any, Tuple
import networkx as nx
from networkx.algorithms import bipartite


class GraphNetworkService:
    def build_bipartite_graph(self, review_records: List[Dict[str, Any]]) -> nx.Graph:
        """
        Builds a bipartite graph B where:
        - Node Set U = Reviewers (bipartite=0)
        - Node Set V = Products (bipartite=1)
        - Edge E = Review link with attributes (rating, date, suspicion_score)
        """
        B = nx.Graph()
        
        for r in review_records:
            reviewer_node = f"rev_{r['reviewer_id']}"
            product_node = f"prod_{r['product_id']}"
            
            # Add Reviewer node
            if not B.has_node(reviewer_node):
                B.add_node(
                    reviewer_node,
                    bipartite=0,
                    node_type="reviewer",
                    label=r.get("reviewer_alias", f"Reviewer {r['reviewer_id']}"),
                    raw_id=r["reviewer_id"],
                    risk_score=r.get("reviewer_anomaly_score", 0.0)
                )
            
            # Add Product node
            if not B.has_node(product_node):
                B.add_node(
                    product_node,
                    bipartite=1,
                    node_type="product",
                    label=r.get("product_title", f"Product {r['product_id']}"),
                    raw_id=r["product_id"],
                    risk_score=100.0 - r.get("product_trust_score", 100.0)
                )
            
            # Add edge
            B.add_edge(
                reviewer_node,
                product_node,
                weight=1.0,
                rating=r.get("rating", 5.0),
                suspicion_score=r.get("suspicion_score", 0.0)
            )
        
        return B

    def project_co_review_graph(self, B: nx.Graph, min_shared_products: int = 1) -> nx.Graph:
        """
        Projects bipartite graph into a single-mode Reviewer-Reviewer co-review graph.
        An edge exists between Reviewer A and Reviewer B if they reviewed the same product(s).
        Edge weight = number of co-reviewed products.
        """
        reviewer_nodes = [n for n, d in B.nodes(data=True) if d.get("bipartite") == 0]
        if not reviewer_nodes:
            return nx.Graph()

        # Weighted projected graph
        co_graph = bipartite.weighted_projected_graph(B, reviewer_nodes)
        
        # Filter edges by minimum shared products threshold
        filtered_graph = nx.Graph()
        for u in co_graph.nodes():
            filtered_graph.add_node(u, **co_graph.nodes[u])
            
        for u, v, data in co_graph.edges(data=True):
            if data.get("weight", 1) >= min_shared_products:
                filtered_graph.add_edge(u, v, **data)
                
        return filtered_graph

    def detect_collusion_clusters(self, co_graph: nx.Graph, min_cluster_size: int = 2) -> List[Dict[str, Any]]:
        """
        Mines connected components and dense cliques in the co-review graph
        to discover suspicious reviewer rings.
        """
        clusters = []
        if co_graph.number_of_nodes() == 0:
            return clusters

        # 1. Connected components with multi-edge density
        components = list(nx.connected_components(co_graph))
        cluster_idx = 1

        for comp in components:
            if len(comp) >= min_cluster_size:
                subg = co_graph.subgraph(comp)
                density = nx.density(subg)
                avg_shared = (
                    sum(d.get("weight", 1) for _, _, d in subg.edges(data=True)) / max(subg.number_of_edges(), 1)
                )
                
                # High density (> 0.4) indicates tightly coordinated behavior
                if density > 0.35 or len(comp) >= 3:
                    # Centrality within cluster
                    centrality = nx.degree_centrality(subg)
                    members = []
                    for node in comp:
                        members.append({
                            "node_id": node,
                            "raw_reviewer_id": subg.nodes[node].get("raw_id"),
                            "label": subg.nodes[node].get("label"),
                            "centrality": round(float(centrality.get(node, 0.0)), 3)
                        })

                    clusters.append({
                        "cluster_name": f"Ring-Cluster-#{cluster_idx:03d}",
                        "member_count": len(comp),
                        "density": round(float(density), 3),
                        "avg_co_reviews": round(float(avg_shared), 2),
                        "members": members
                    })
                    cluster_idx += 1

        return clusters

    def export_graph_for_visualization(self, B: nx.Graph, clusters: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exports the graph to JSON format compatible with React network visualization
        libraries (Cytoscape / VisNetwork).
        """
        # Map reviewers to detected clusters
        cluster_map = {}
        if clusters:
            for c in clusters:
                for m in c["members"]:
                    cluster_map[m["node_id"]] = c["cluster_name"]

        nodes = []
        for n, data in B.nodes(data=True):
            node_type = data.get("node_type", "reviewer")
            risk_score = data.get("risk_score", 0.0)
            group_name = cluster_map.get(n, "Normal" if node_type == "reviewer" else "Product")
            
            nodes.append({
                "id": str(n),
                "label": str(data.get("label", n)),
                "node_type": node_type,
                "risk_score": float(risk_score),
                "group": group_name,
                "metadata": {
                    "raw_id": data.get("raw_id"),
                    "bipartite": data.get("bipartite")
                }
            })

        edges = []
        for u, v, data in B.edges(data=True):
            edges.append({
                "id": f"{u}->{v}",
                "source": str(u),
                "target": str(v),
                "weight": float(data.get("weight", 1.0)),
                "edge_type": "reviewed",
                "metadata": {
                    "rating": data.get("rating", 5.0),
                    "suspicion_score": data.get("suspicion_score", 0.0)
                }
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "detected_clusters_count": len(clusters) if clusters else 0
        }


graph_service = GraphNetworkService()
