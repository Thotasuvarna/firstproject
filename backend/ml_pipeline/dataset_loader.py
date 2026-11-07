"""
Dataset Generator & Preprocessor for Fake Review Benchmarking.
Generates realistic labeled corpora combining deceptive opinion spam patterns
and legitimate organic reviews across diverse product categories.
"""
import pandas as pd
import numpy as np


def generate_benchmark_dataset(num_samples: int = 1200, random_seed: int = 42) -> pd.DataFrame:
    """
    Constructs a labeled benchmark dataset based on real-world deceptive review patterns.
    Label: 0 = Organic / Genuine, 1 = Deceptive / Fake
    """
    np.random.seed(random_seed)

    # Truthful organic review templates (varied tone, specific product details, balanced ratings)
    organic_samples = [
        ("The battery life on this laptop lasts about 6 to 7 hours of standard browsing. Keys feel slightly mushy but acceptable for the price.", 3.5, 1),
        ("Assembly took around 45 minutes with the included hex wrench. Solid build quality, though the instructions were a bit sparse.", 4.0, 1),
        ("Sound quality is clear on mids and highs, but the low-end bass is noticeably lacking compared to my previous Sony headphones.", 3.0, 1),
        ("After three weeks of daily kitchen use, the non-stick coating started peeling near the rim. Disappointed and returning.", 1.5, 1),
        ("Great ergonomic mouse! Relieved my wrist fatigue during 8-hour work days. Software setup was smooth on Windows 11.", 5.0, 1),
        ("Decent cotton t-shirt, fits true to size. Shrinks slightly after the first wash, so consider sizing up if you like a loose fit.", 4.0, 1),
        ("Received with a cracked screen protector in the package. Customer support replaced it promptly within 3 business days.", 3.5, 1),
        ("The coffee maker works as expected. Fast brew time of 4 minutes for a full pot. Carafe spout doesn't drip.", 4.5, 1),
        ("Colors on the monitor are vibrant after calibrating the ICC profile. Minimal backlight bleed on the bottom left corner.", 4.0, 1),
        ("Bluetooth disconnects intermittently when moving more than 15 feet away from the phone. Otherwise sound is good.", 3.0, 1)
    ]

    # Deceptive / Promotional spam templates (hyperbolic praise, vague superlatives, template duplicates, extreme 5.0 stars)
    deceptive_samples = [
        ("AMAZING BEST PRODUCT EVER! MUST BUY! 100% SATISFIED! AMAZING AMAZING QUALITY! WOW!", 5.0, 0),
        ("Top notch superb quality item, best in class, absolutely flawless, everyone must purchase this immediately!", 5.0, 0),
        ("Completely transformed my life! Best seller on the entire platform. Highest possible recommendation!", 5.0, 0),
        ("Great item great price great delivery great store will buy again and again!", 5.0, 0),
        ("DO NOT BUY TOTAL SCAM TRASH HORRIBLE BROKE IN ONE MINUTE WORST STORE EVER FRAUD!", 1.0, 0),
        ("Very good quality, I love this product so much. Perfect item and five star seller!", 5.0, 0),
        ("Best quality on the market! Five stars! Buy with complete confidence!", 5.0, 0),
        ("Outstanding product! Exceeded all my expectations! Highly recommend to all friends and family!", 5.0, 0),
        ("Horrible awful disaster, defective broken junk scam fake counterfeit!", 1.0, 0),
        ("Spectacular marvelous unbelievable perfection! Top rated product of the millennium!", 5.0, 0)
    ]

    rows = []
    
    # Generate balanced dataset
    n_per_class = num_samples // 2

    # Genuine class (0)
    for i in range(n_per_class):
        base_text, base_rating, verified = organic_samples[i % len(organic_samples)]
        # Add slight variations
        rating_jitter = np.clip(base_rating + np.random.choice([-0.5, 0.0, 0.5]), 1.0, 5.0)
        verified_prob = 1 if np.random.rand() > 0.15 else 0
        rows.append({
            "review_text": base_text,
            "rating": rating_jitter,
            "is_verified_purchase": verified_prob,
            "label": 0
        })

    # Deceptive class (1)
    for i in range(n_per_class):
        base_text, base_rating, verified = deceptive_samples[i % len(deceptive_samples)]
        rating_val = 5.0 if np.random.rand() > 0.2 else 1.0
        verified_prob = 0 if np.random.rand() > 0.20 else 1  # Often unverified
        rows.append({
            "review_text": base_text,
            "rating": rating_val,
            "is_verified_purchase": verified_prob,
            "label": 1
        })

    df = pd.DataFrame(rows)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    return df
