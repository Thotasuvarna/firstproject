"""
Comprehensive Database Seeding Script.
Populates admin accounts, products, legitimate organic reviews,
linguistic spam outliers, and a coordinated reviewer collusion ring.
"""
from datetime import datetime, timedelta, timezone
from app.core.database import SessionLocal, init_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.product import ProductCreate
from app.schemas.review import ReviewCreate
from app.api.v1.products import create_product
from app.api.v1.reviews import process_and_save_review
from app.api.v1.graph import get_network_graph


def seed_database():
    print("[Seeder] Initializing database schema...")
    init_db()
    db = SessionLocal()

    try:
        # 1. Seed Users
        if db.query(User).count() == 0:
            print("[Seeder] Creating admin and analyst user accounts...")
            admin = User(
                email="admin@antigravity.io",
                hashed_password=hash_password("Admin@12345"),
                full_name="Chief Information Security Officer",
                role="admin",
                is_active=True
            )
            analyst = User(
                email="analyst@antigravity.io",
                hashed_password=hash_password("Analyst@12345"),
                full_name="Lead Trust & Safety Auditor",
                role="analyst",
                is_active=True
            )
            db.add_all([admin, analyst])
            db.commit()
            print("  -> Admin: admin@antigravity.io / Admin@12345")
            print("  -> Analyst: analyst@antigravity.io / Analyst@12345")

        admin_user = db.query(User).first()

        # 2. Seed Products
        products = [
            ("TECH-SONY-XM5", "Sony WH-1000XM5 Wireless Noise-Canceling Headphones", "Electronics", "Industry leading active noise canceling headphones with 30-hour battery life."),
            ("TECH-IPHONE-15", "Apple iPhone 15 Pro 256GB Titanium", "Smartphones", "Flagship smartphone featuring aerospace-grade titanium design and A17 Pro chip."),
            ("HOME-SMART-PLUG", "EvoSmart Wi-Fi Smart Power Plug", "Smart Home", "Compact smart plug compatible with Alexa and Google Assistant."),
            ("FIT-PULSE-TRACK", "PulseTrack Active Fitness Tracker Band", "Wearables", "Waterproof fitness band with continuous heart rate and SpO2 tracking.")
        ]

        for sku, title, cat, desc in products:
            try:
                create_product(ProductCreate(product_sku=sku, title=title, category=cat, description=desc), db=db, current_user=admin_user)
            except Exception:
                pass  # Already exists

        print("[Seeder] Ingesting authentic organic reviews...")
        organic_reviews = [
            ("TECH-SONY-XM5", "marcus.k@audiotech.net", 4.5, "Incredible noise isolation", "The ANC on airplanes is unrivaled. Soundstage is slightly warmer than XM4s, but battery easily lasts my international flights.", True),
            ("TECH-SONY-XM5", "sarah.j91@gmail.com", 3.5, "Comfortable but warm earcups", "Sound is crisp and call microphone is surprisingly clear. However, my ears get warm after about two hours of continuous use.", True),
            ("TECH-IPHONE-15", "david.chen@enterprise.io", 4.0, "Substantial weight reduction", "The titanium frame makes a noticeable ergonomic difference in daily hand fatigue. Action button is convenient for flashlight.", True),
            ("FIT-PULSE-TRACK", "rachel.runner@yahoo.com", 4.0, "Great value fitness tracker", "Step count matches my treadmill within 3% accuracy. Sleep tracker accurately detects REM cycles.", True)
        ]

        now = datetime.now(timezone.utc)

        for sku, rev_id, rating, title, text, verified in organic_reviews:
            process_and_save_review(ReviewCreate(
                product_sku=sku,
                reviewer_identifier=rev_id,
                rating=rating,
                review_title=title,
                review_text=text,
                review_date=now - timedelta(days=12),
                is_verified_purchase=verified
            ), db=db)

        print("[Seeder] Ingesting duplicate template spam & cognitive dissonance outliers...")
        spam_duplicates = [
            ("HOME-SMART-PLUG", "spambot_promo_01@darkmail.cc", 5.0, "BEST QUALITY MUST BUY", "AMAZING PRODUCT! Completely transformed my home, highest quality, best seller on the platform, five stars recommend to everyone!", False),
            ("HOME-SMART-PLUG", "spambot_promo_02@darkmail.cc", 5.0, "HIGHLY RECOMMEND 5 STARS", "AMAZING PRODUCT! Completely transformed my home, highest quality, best seller on the platform, five stars recommend to everyone!", False),
            ("HOME-SMART-PLUG", "spambot_promo_03@darkmail.cc", 5.0, "MUST BUY TODAY", "AMAZING PRODUCT! Completely transformed my home, highest quality, best seller on the platform, five stars recommend to everyone!", False),
            ("TECH-SONY-XM5", "dissatisfied_bot@spamhub.com", 5.0, "Total Scam", "Terrible broken garbage, defective junk, horrible seller scam fake counterfeit!", False)
        ]

        for sku, rev_id, rating, title, text, verified in spam_duplicates:
            process_and_save_review(ReviewCreate(
                product_sku=sku,
                reviewer_identifier=rev_id,
                rating=rating,
                review_title=title,
                review_text=text,
                review_date=now - timedelta(hours=3),
                is_verified_purchase=verified
            ), db=db)

        print("[Seeder] Simulating Coordinated Reviewer Collusion Ring (4 accounts attacking 2 products)...")
        # Collusion ring: accounts A, B, C, D co-reviewing HOME-SMART-PLUG and FIT-PULSE-TRACK in bursts
        collusion_accounts = [
            "collusion_sybil_01@botnet.ru",
            "collusion_sybil_02@botnet.ru",
            "collusion_sybil_03@botnet.ru",
            "collusion_sybil_04@botnet.ru"
        ]

        for acc in collusion_accounts:
            # Review Product 1
            process_and_save_review(ReviewCreate(
                product_sku="HOME-SMART-PLUG",
                reviewer_identifier=acc,
                rating=5.0,
                review_title="Superb Smart Device",
                review_text="Fantastic smart plug, setup in 10 seconds, highest recommendation for all smart home users!",
                review_date=now - timedelta(minutes=45),
                is_verified_purchase=False
            ), db=db)

            # Review Product 2
            process_and_save_review(ReviewCreate(
                product_sku="FIT-PULSE-TRACK",
                reviewer_identifier=acc,
                rating=5.0,
                review_title="Flawless tracker",
                review_text="Incredible battery and build quality, perfect accuracy, top rated seller!",
                review_date=now - timedelta(minutes=30),
                is_verified_purchase=False
            ), db=db)

        db.commit()

        # Run network graph detection to link clusters
        print("[Seeder] Running NetworkX graph clustering on populated database...")
        graph_data = get_network_graph(min_shared=1, limit=500, db=db)
        print(f"[Seeder] Successfully analyzed graph: {graph_data['total_nodes']} nodes, {graph_data['total_edges']} edges, {graph_data['detected_clusters_count']} collusion rings discovered!")

        print("\n" + "=" * 60)
        print("DATABASE SEEDING COMPLETE!")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
