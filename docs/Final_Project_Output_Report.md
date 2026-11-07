# SENTINEL AI: Final Project Output Dossier
## AI-Powered Fake Review and Coordinated Reviewer Network Detection System

---

## 1. Executive Deliverables Summary

The **Sentinel AI** platform has been implemented, validated, and evaluated end-to-end. It integrates Natural Language Processing (NLP), Supervised Machine Learning, NetworkX Bipartite Graph Mining, and Explainable AI (XAI) into a cohesive full-stack web application.

- **Backend Service**: Python 3.14 + FastAPI + SQLAlchemy ORM (MySQL / SQLite)
- **Frontend Client**: React 18 + Vite + Vis.js Network Physics Engine
- **Test Suite**: 7/7 Unit & Integration Tests Passing (100% pass rate)
- **Champion ML Model**: Logistic Regression ($F1 = 1.0000$, $\text{ROC-AUC} = 1.0000$)
- **Generated Forensic Audit Dossier**: [generated_audit_dossier.pdf](file:///C:/Users/THOTA%20SUVARNA/.gemini/antigravity/brain/cbdcb1ea-3fa2-415b-8722-669bff3ceced/generated_audit_dossier.pdf)

---

## 2. Live API Output & Execution Metrics

### 2.1 Threat Intelligence Dashboard (`GET /api/v1/dashboard/metrics`)
```json
{
  "total_reviews": 16,
  "suspicious_reviews_count": 10,
  "suspicious_reviews_percentage": 62.5,
  "total_products": 4,
  "total_reviewers": 12,
  "detected_clusters_count": 2,
  "average_trust_score": 77.5,
  "risk_tier_breakdown": {
    "HIGH": 0,
    "MEDIUM": 10,
    "LOW": 6
  },
  "top_flagged_products": [
    {
      "id": 3,
      "sku": "HOME-SMART-PLUG",
      "title": "EvoSmart Wi-Fi Smart Power Plug",
      "trust_score": 54.4,
      "total_reviews": 7,
      "avg_rating": 5.0
    },
    {
      "id": 4,
      "sku": "FIT-PULSE-TRACK",
      "title": "PulseTrack Active Fitness Tracker Band",
      "trust_score": 60.2,
      "total_reviews": 5,
      "avg_rating": 4.8
    },
    {
      "id": 1,
      "sku": "TECH-SONY-XM5",
      "title": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones",
      "trust_score": 95.2,
      "total_reviews": 3,
      "avg_rating": 4.33
    },
    {
      "id": 2,
      "sku": "TECH-IPHONE-15",
      "title": "Apple iPhone 15 Pro 256GB Titanium",
      "trust_score": 100.0,
      "total_reviews": 1,
      "avg_rating": 4.0
    }
  ]
}
```

---

### 2.2 NetworkX Bipartite Topology & Collusion Mining (`GET /api/v1/graph/network`)
```json
{
  "total_nodes": 16,
  "total_edges": 16,
  "detected_clusters_count": 2,
  "cluster_breakdown": [
    {
      "cluster_name": "Ring-Cluster-#001",
      "member_count": 4,
      "collusion_density": 1.0,
      "target_products": ["HOME-SMART-PLUG", "FIT-PULSE-TRACK"],
      "status": "DETECTED"
    }
  ]
}
```

---

### 2.3 Real-Time Review Scan with Explainable AI (`POST /api/v1/reviews`)
**Input Payload**:
```json
{
  "product_sku": "HOME-SMART-PLUG",
  "reviewer_identifier": "spambot_promo_01@darkmail.cc",
  "rating": 5.0,
  "review_title": "BEST QUALITY MUST BUY",
  "review_text": "AMAZING PRODUCT! Completely transformed my home, highest quality, best seller on the platform, five stars recommend to everyone!",
  "is_verified_purchase": false
}
```

**Real-Time Output**:
```json
{
  "review_id": 6,
  "product_id": 3,
  "composite_suspicion_score": 54.8,
  "risk_tier": "MEDIUM",
  "explainability_factors": {
    "score": 54.8,
    "risk_tier": "MEDIUM",
    "primary_drivers": [
      {
        "factor": "High Duplicate Similarity",
        "severity": "CRITICAL",
        "impact_percentage": 25,
        "description": "Text has 100% lexical match with another review on record."
      },
      {
        "factor": "Unverified Purchase",
        "severity": "INFO",
        "impact_percentage": 5,
        "description": "Review originated from an unverified customer account."
      }
    ],
    "component_breakdown": {
      "duplicate_similarity": 1.0,
      "sentiment_divergence": 0.0,
      "burst_velocity": 0.0,
      "rating_extremity": 1.0,
      "ml_probability": 0.992,
      "is_unverified": true,
      "is_cluster_member": false
    }
  }
}
```

---

## 3. Supervised Machine Learning Benchmark

Stratified holdout validation ($N = 1,600$ reviews; Train: $1,200$, Test: $400$):

| Model Architecture | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Logistic Regression (L2 Regularized)** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **Random Forest (100 Trees, Depth=12)** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Gradient Boosting Classifier** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

*Champion Model Artifact*: `backend/saved_models/champion_model.joblib` (Includes TF-IDF Vectorizer + Trained Estimator).

---

## 4. Verification & Automated Test Suite Output

Execution of `pytest tests/test_backend.py -v -o norecursedirs=venv`:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0
cachedir: .pytest_cache
rootdir: C:\Users\THOTA SUVARNA\.gemini\antigravity\scratch\fake-review-network-detector\backend
configfile: pytest.ini
collected 7 items

tests/test_backend.py::test_pseudonymization_privacy PASSED              [ 14%]
tests/test_backend.py::test_password_hashing_and_jwt PASSED              [ 28%]
tests/test_backend.py::test_nlp_duplicate_and_sentiment PASSED           [ 42%]
tests/test_backend.py::test_graph_network_collusion_mining PASSED        [ 57%]
tests/test_backend.py::test_explainable_scoring PASSED                   [ 71%]
tests/test_backend.py::test_api_workflow_end_to_end PASSED               [ 85%]
tests/test_backend.py::test_pdf_report_generation PASSED                 [100%]

============================== 7 passed in 6.58s ==============================
```
