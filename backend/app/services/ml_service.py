"""
Machine Learning Inference Service.
Loads the trained Champion Model artifact and computes real-time predictions.
"""
import os
import joblib
import numpy as np
from scipy.sparse import hstack
from typing import Tuple, Dict, Any, Optional

from app.services.nlp_service import nlp_service


class MLInferenceService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_name = "Rule-based Fallback"
        self.metrics = {}
        self._load_model()

    def _load_model(self):
        """Attempts to load saved champion model artifact."""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "saved_models",
            "champion_model.joblib"
        )
        if os.path.exists(model_path):
            try:
                bundle = joblib.load(model_path)
                self.model = bundle["model"]
                self.vectorizer = bundle["vectorizer"]
                self.model_name = bundle.get("model_name", "Trained ML Model")
                self.metrics = bundle.get("metrics", {})
            except Exception:
                pass

    def predict_deception_probability(
        self,
        review_text: str,
        rating: float,
        is_verified_purchase: bool
    ) -> float:
        """
        Runs feature extraction and computes predicted probability of deception (0.0 to 1.0).
        """
        if self.model is None or self.vectorizer is None:
            # Fallback heuristic if model is not yet compiled
            sty = nlp_service.extract_stylometrics(review_text)
            sentiment = nlp_service.calculate_sentiment(review_text)
            div = nlp_service.calculate_rating_divergence(rating, sentiment)
            fallback_score = (div * 0.4) + (sty["caps_ratio"] * 0.3) + (0.3 if not is_verified_purchase else 0.0)
            return round(float(np.clip(fallback_score, 0.0, 1.0)), 3)

        # 1. Text TF-IDF vectorization
        clean_text = nlp_service.clean_text(review_text)
        X_tfidf = self.vectorizer.transform([clean_text])

        # 2. Dense features
        sty = nlp_service.extract_stylometrics(review_text)
        sentiment = nlp_service.calculate_sentiment(review_text)
        divergence = nlp_service.calculate_rating_divergence(rating, sentiment)

        dense_vec = np.array([[
            rating,
            1.0 if is_verified_purchase else 0.0,
            sty["length"] / 500.0,
            sty["exclamation_density"] * 10.0,
            sty["caps_ratio"] * 10.0,
            sty["lexical_diversity"],
            sentiment,
            divergence
        ]])

        # 3. Combine sparse + dense
        X_combined = hstack([X_tfidf, dense_vec]).tocsr()

        # 4. Predict probability
        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(X_combined)[0, 1]
        else:
            prob = float(self.model.predict(X_combined)[0])

        return round(float(prob), 3)


ml_service = MLInferenceService()
