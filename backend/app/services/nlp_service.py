"""
Natural Language Processing (NLP) & Stylometrics Service.
- Text normalization & cleaning
- TF-IDF and Cosine Similarity for duplicate / template detection
- Sentiment & Rating Divergence analysis
- Stylometric markers (capitalization, punctuation intensity, lexical diversity)
"""
import re
import math
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class NLPService:
    def __init__(self):
        # Common English stopwords list to avoid external heavy downloads
        self.stopwords = {
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
            "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
            "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
            "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
            "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
            "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", 
            "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", 
            "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", 
            "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", 
            "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", 
            "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", 
            "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", 
            "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", 
            "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", 
            "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", 
            "you're", "you've", "your", "yours", "yourself", "yourselves"
        }
        
        # Sentiment lexicon for polarity scoring
        self.positive_lexicon = {
            "good", "great", "excellent", "amazing", "wonderful", "fantastic", "awesome", "love", "loved",
            "best", "perfect", "superb", "outstanding", "exceptional", "helpful", "reliable", "genuine",
            "impressed", "flawless", "durable", "high-quality", "delighted", "recommend", "brilliant"
        }
        self.negative_lexicon = {
            "bad", "terrible", "horrible", "awful", "worst", "poor", "broken", "waste", "disappointed",
            "disappointing", "scam", "fake", "defective", "useless", "cheap", "damaged", "trash", "crap",
            "hate", "hated", "slow", "failed", "unreliable", "pathetic", "garbage", "counterfeit"
        }

    def clean_text(self, text: str) -> str:
        """Sanitize text, remove punctuation, and lowercase."""
        if not text:
            return ""
        text = text.lower()
        # Remove URLs and special characters
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        tokens = [word for word in text.split() if word not in self.stopwords and len(word) > 1]
        return " ".join(tokens)

    def extract_stylometrics(self, raw_text: str) -> Dict[str, float]:
        """
        Extract stylistic writing patterns:
        - Excessive exclamation or question marks
        - Capital letter shouting ratio
        - Lexical diversity (unique words / total words)
        - Text length
        """
        if not raw_text:
            return {"length": 0, "exclamation_density": 0.0, "caps_ratio": 0.0, "lexical_diversity": 0.0}
        
        total_chars = max(len(raw_text), 1)
        exclamation_count = raw_text.count("!") + raw_text.count("?")
        uppercase_count = sum(1 for c in raw_text if c.isupper())
        
        words = raw_text.split()
        total_words = max(len(words), 1)
        unique_words = len(set(w.lower() for w in words))
        
        return {
            "length": float(total_chars),
            "word_count": float(total_words),
            "exclamation_density": round(exclamation_count / total_chars, 4),
            "caps_ratio": round(uppercase_count / total_chars, 4),
            "lexical_diversity": round(unique_words / total_words, 4)
        }

    def calculate_sentiment(self, text: str) -> float:
        """
        Computes sentiment polarity between -1.0 (strongly negative) to +1.0 (strongly positive).
        """
        cleaned = self.clean_text(text)
        words = cleaned.split()
        if not words:
            return 0.0
            
        pos_hits = sum(1 for w in words if w in self.positive_lexicon)
        neg_hits = sum(1 for w in words if w in self.negative_lexicon)
        
        total_sentiment_words = pos_hits + neg_hits
        if total_sentiment_words == 0:
            return 0.0
        
        polarity = (pos_hits - neg_hits) / total_sentiment_words
        return round(float(polarity), 3)

    def calculate_rating_divergence(self, rating: float, sentiment_polarity: float) -> float:
        """
        Measures cognitive dissonance between star rating (1 to 5) and sentiment (-1 to +1).
        Normalized rating: 1 star -> -1.0, 3 stars -> 0.0, 5 stars -> +1.0.
        Divergence score ranges from 0.0 (perfect harmony) to 1.0 (maximum discord).
        """
        normalized_rating = (rating - 3.0) / 2.0  # Maps 1..5 to -1..+1
        # Absolute difference between tone and rating
        divergence = abs(normalized_rating - sentiment_polarity) / 2.0  # Max diff is 2.0, so divide by 2
        return round(float(np.clip(divergence, 0.0, 1.0)), 3)

    def calculate_duplicate_similarity(self, target_text: str, corpus_texts: List[str]) -> Tuple[float, Optional[str]]:
        """
        Computes the maximum TF-IDF Cosine Similarity between the target review
        and all existing reviews in the corpus.
        Returns: (highest_similarity_score [0..1], matched_sample_or_None)
        """
        clean_target = self.clean_text(target_text)
        if not clean_target or not corpus_texts:
            return 0.0, None

        cleaned_corpus = [self.clean_text(t) for t in corpus_texts if t.strip()]
        if not cleaned_corpus:
            return 0.0, None

        all_docs = [clean_target] + cleaned_corpus
        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
            tfidf_matrix = vectorizer.fit_transform(all_docs)
            
            # Compute cosine similarity between target (index 0) and corpus (index 1..)
            target_vec = tfidf_matrix[0:1]
            corpus_vecs = tfidf_matrix[1:]
            
            sim_scores = cosine_similarity(target_vec, corpus_vecs).flatten()
            max_idx = int(np.argmax(sim_scores))
            max_sim = float(sim_scores[max_idx])
            
            matched_text = corpus_texts[max_idx] if max_sim > 0.65 else None
            return round(max_sim, 3), matched_text
        except Exception:
            return 0.0, None


nlp_service = NLPService()
