"""
Explainable AI (XAI) Suspicious Scoring Engine.
Synthesizes NLP, ML inference probability, behavioral metrics, and graph collusion indicators
into a transparent, justifiable suspicion score (0-100) with clear explanatory factors.
"""
from typing import Dict, Any, List, Tuple


class ExplainableScoringService:
    def __init__(self):
        # Weights for composite score aggregation (sum = 1.0)
        self.weights = {
            "duplicate_similarity": 0.25,  # Plagiarism / copy-paste reviews
            "sentiment_divergence": 0.15,  # Rating-text cognitive dissonance
            "burst_velocity": 0.15,        # Speed posting anomaly
            "rating_extremity": 0.10,      # Polarized 1 or 5 star bias
            "unverified_purchase": 0.05,   # Not an authenticated buyer
            "ml_model_prob": 0.15,         # Trained ML Classifier prediction
            "cluster_collusion": 0.15      # Network collusion ring membership
        }

    def compute_composite_score(
        self,
        duplicate_similarity: float,  # 0.0 to 1.0
        sentiment_divergence: float,  # 0.0 to 1.0
        burst_velocity: float,        # 0.0 to 1.0
        rating_extremity: float,      # 0.0 to 1.0
        is_verified_purchase: bool,
        ml_prob: float = 0.0,         # 0.0 to 1.0 from ML model
        is_in_collusion_cluster: bool = False,
        cluster_density: float = 0.0
    ) -> Tuple[float, str, Dict[str, Any]]:
        """
        Calculates normalized Suspicion Score (0..100), Risk Tier,
        and evidence breakdown factors for human auditor transparency.
        """
        unverified_val = 0.0 if is_verified_purchase else 1.0
        cluster_val = min(1.0, cluster_density * 1.5) if is_in_collusion_cluster else 0.0

        # Weighted calculation
        raw_score = (
            (duplicate_similarity * self.weights["duplicate_similarity"]) +
            (sentiment_divergence * self.weights["sentiment_divergence"]) +
            (burst_velocity * self.weights["burst_velocity"]) +
            (rating_extremity * self.weights["rating_extremity"]) +
            (unverified_val * self.weights["unverified_purchase"]) +
            (ml_prob * self.weights["ml_model_prob"]) +
            (cluster_val * self.weights["cluster_collusion"])
        ) * 100.0

        composite_score = round(float(min(max(raw_score, 0.0), 100.0)), 1)

        # Risk Tier categorization
        if composite_score >= 65.0:
            risk_tier = "HIGH"
        elif composite_score >= 35.0:
            risk_tier = "MEDIUM"
        else:
            risk_tier = "LOW"

        # Explainability evidence list
        reasons: List[Dict[str, Any]] = []
        
        if duplicate_similarity >= 0.70:
            reasons.append({
                "factor": "High Duplicate Similarity",
                "severity": "CRITICAL",
                "impact_percentage": int(self.weights["duplicate_similarity"] * 100),
                "description": f"Text has {int(duplicate_similarity * 100)}% lexical match with another review on record."
            })
        elif duplicate_similarity >= 0.40:
            reasons.append({
                "factor": "Moderate Text Re-use",
                "severity": "MODERATE",
                "impact_percentage": int(self.weights["duplicate_similarity"] * 50),
                "description": f"Contains template-like phrasing common across multiple reviews ({int(duplicate_similarity * 100)}% match)."
            })

        if ml_prob >= 0.65:
            reasons.append({
                "factor": "AI Model Deception Flag",
                "severity": "HIGH",
                "impact_percentage": int(self.weights["ml_model_prob"] * 100),
                "description": f"Supervised ML classifier flagged text patterns as deceptive (confidence: {int(ml_prob * 100)}%)."
            })

        if sentiment_divergence >= 0.60:
            reasons.append({
                "factor": "Rating vs. Tone Dissonance",
                "severity": "HIGH",
                "impact_percentage": int(self.weights["sentiment_divergence"] * 100),
                "description": "Star rating strongly conflicts with textual sentiment polarity."
            })

        if burst_velocity >= 0.70:
            reasons.append({
                "factor": "Burst Posting Velocity",
                "severity": "HIGH",
                "impact_percentage": int(self.weights["burst_velocity"] * 100),
                "description": "Reviewer submitted an abnormal cluster of reviews in a tight temporal window."
            })

        if is_in_collusion_cluster:
            reasons.append({
                "factor": "Coordinated Ring Member",
                "severity": "CRITICAL",
                "impact_percentage": int(self.weights["cluster_collusion"] * 100),
                "description": f"Reviewer belongs to a detected co-review collusion network (density: {cluster_density:.2f})."
            })

        if not is_verified_purchase:
            reasons.append({
                "factor": "Unverified Purchase",
                "severity": "INFO",
                "impact_percentage": int(self.weights["unverified_purchase"] * 100),
                "description": "Review originated from an unverified customer account."
            })

        explainability = {
            "score": composite_score,
            "risk_tier": risk_tier,
            "primary_drivers": reasons,
            "component_breakdown": {
                "duplicate_similarity": round(duplicate_similarity, 3),
                "sentiment_divergence": round(sentiment_divergence, 3),
                "burst_velocity": round(burst_velocity, 3),
                "rating_extremity": round(rating_extremity, 3),
                "ml_probability": round(ml_prob, 3),
                "is_unverified": not is_verified_purchase,
                "is_cluster_member": is_in_collusion_cluster
            }
        }

        return composite_score, risk_tier, explainability


scoring_service = ExplainableScoringService()
