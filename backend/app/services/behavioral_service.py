"""
Behavioral Anomaly Detection Service.
Analyzes posting velocity, rating bias, and deviation from product baseline.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class BehavioralService:
    def calculate_velocity_anomaly(self, reviewer_recent_dates: List[datetime], window_hours: int = 24) -> float:
        """
        Calculates burstiness score.
        If a reviewer posts an unusually high volume of reviews within a narrow window (e.g. > 5 in 24h),
        burst score escalates towards 1.0.
        """
        if not reviewer_recent_dates or len(reviewer_recent_dates) <= 1:
            return 0.0

        clean_dates = [d.replace(tzinfo=None) if d.tzinfo is not None else d for d in reviewer_recent_dates]
        sorted_dates = sorted(clean_dates)
        now = sorted_dates[-1]
        threshold_time = now - timedelta(hours=window_hours)
        burst_count = sum(1 for d in sorted_dates if d >= threshold_time)

        if burst_count <= 2:
            return 0.0
        elif burst_count <= 5:
            return 0.35
        elif burst_count <= 10:
            return 0.70
        else:
            return 1.0

    def calculate_rating_extremity(self, reviewer_all_ratings: List[float]) -> float:
        """
        Reviews that are exclusively 5.0 or 1.0 with no nuanced ratings (2, 3, 4)
        exhibit high rating polarity bias typical of incentivized or smear campaigns.
        """
        if not reviewer_all_ratings:
            return 0.0
        
        extreme_count = sum(1 for r in reviewer_all_ratings if r >= 4.8 or r <= 1.2)
        extremity_ratio = extreme_count / len(reviewer_all_ratings)
        return round(float(extremity_ratio), 3)

    def calculate_product_rating_deviation(self, review_rating: float, product_avg_rating: float) -> float:
        """
        Measures how far a specific review diverges from the established crowd consensus.
        Normalized to [0..1].
        """
        if product_avg_rating <= 0:
            return 0.0
        deviation = abs(review_rating - product_avg_rating) / 4.0  # Max delta on 1..5 scale is 4.0
        return round(float(min(deviation, 1.0)), 3)


behavioral_service = BehavioralService()
