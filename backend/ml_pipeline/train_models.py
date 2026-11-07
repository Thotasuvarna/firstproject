"""
Machine Learning Training & Comparative Evaluation Pipeline.
Trains multiple classification models (Logistic Regression, Random Forest, Gradient Boosting),
evaluates on holdout test set (Precision, Recall, F1, ROC-AUC), and saves champion model.
"""
import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from ml_pipeline.dataset_loader import generate_benchmark_dataset
from app.services.nlp_service import nlp_service


def extract_feature_matrix(df: pd.DataFrame, vectorizer: TfidfVectorizer = None, is_train: bool = True):
    """
    Extracts multimodal feature matrix:
    - Text TF-IDF N-grams (1, 2)
    - Rating & Verified Purchase status
    - Stylometric ratios (length, caps, punctuation, lexical diversity)
    - Sentiment polarity & rating divergence
    """
    # 1. Text TF-IDF
    cleaned_texts = [nlp_service.clean_text(t) for t in df["review_text"]]
    
    if is_train:
        vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        X_tfidf = vectorizer.fit_transform(cleaned_texts)
    else:
        X_tfidf = vectorizer.transform(cleaned_texts)

    # 2. Dense Stylometric & Behavioral Features
    dense_features = []
    for _, row in df.iterrows():
        text = str(row["review_text"])
        rating = float(row["rating"])
        verified = float(row["is_verified_purchase"])
        
        # Stylometrics
        sty = nlp_service.extract_stylometrics(text)
        sentiment = nlp_service.calculate_sentiment(text)
        divergence = nlp_service.calculate_rating_divergence(rating, sentiment)
        
        dense_features.append([
            rating,
            verified,
            sty["length"] / 500.0,
            sty["exclamation_density"] * 10.0,
            sty["caps_ratio"] * 10.0,
            sty["lexical_diversity"],
            sentiment,
            divergence
        ])
    
    X_dense = np.array(dense_features)
    # Combine sparse TF-IDF with dense features
    X_combined = hstack([X_tfidf, X_dense]).tocsr()
    
    return X_combined, vectorizer


def train_and_evaluate_models():
    """Executes end-to-end ML training and model comparison."""
    print("=" * 70)
    print("1. Loading Benchmark Fake Review Dataset...")
    df = generate_benchmark_dataset(num_samples=1600, random_seed=42)
    print(f"Loaded {len(df)} review samples (Class Balance: {df['label'].value_counts().to_dict()})")

    # Split train / test with stratification (prevents data leakage)
    train_df, test_df = train_test_split(
        df, test_size=0.25, stratify=df["label"], random_state=42
    )
    print(f"Training Samples: {len(train_df)}, Holdout Test Samples: {len(test_df)}")

    # Extract features
    print("2. Extracting TF-IDF & Stylometric Feature Matrices...")
    X_train, vectorizer = extract_feature_matrix(train_df, is_train=True)
    X_test, _ = extract_feature_matrix(test_df, vectorizer=vectorizer, is_train=False)

    y_train = train_df["label"].values
    y_test = test_df["label"].values

    # Define Candidate Models
    models = {
        "Logistic Regression": LogisticRegression(C=1.0, max_iter=500, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting Classifier": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    }

    results = []
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None

    print("\n3. Training & Evaluating Candidate Models...")
    print("-" * 70)
    print(f"{'Model':<30} | {'Accuracy':<8} | {'Precision':<9} | {'Recall':<6} | {'F1-Score':<8} | {'ROC-AUC':<7}")
    print("-" * 70)

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)

        print(f"{name:<30} | {acc:.4f}   | {prec:.4f}    | {rec:.4f} | {f1:.4f}   | {auc:.4f}")

        results.append({
            "model_name": name,
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "roc_auc": auc
        })

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model

    print("-" * 70)
    print(f"\nChampion Model Selected: {best_model_name} (F1-Score: {best_f1:.4f})")

    # Save artifacts
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_models")
    os.makedirs(save_dir, exist_ok=True)
    model_path = os.path.join(save_dir, "champion_model.joblib")

    artifact_bundle = {
        "model": best_model_obj,
        "model_name": best_model_name,
        "vectorizer": vectorizer,
        "metrics": next(r for r in results if r["model_name"] == best_model_name)
    }
    joblib.dump(artifact_bundle, model_path)
    print(f"Saved Champion Model Artifact bundle to: {model_path}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    train_and_evaluate_models()
