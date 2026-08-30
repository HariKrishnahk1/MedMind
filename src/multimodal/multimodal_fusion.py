"""
Multimodal Clinical Fusion Engine.

Combines numerical/time-series clinical feature vectors with clinical text embeddings
into a unified multimodal patient representation for deterioration probability prediction.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from src.multimodal.clinical_text_extractor import extract_clinical_concepts_from_note

class MultimodalFusionEngine:
    def __init__(self, max_text_features: int = 10):
        self.max_text_features = max_text_features
        self.vectorizer = TfidfVectorizer(max_features=max_text_features, stop_words="english")
        self.is_fit = False

    def fit_text_encoder(self, notes: List[str]):
        if notes:
            self.vectorizer.fit(notes)
            self.is_fit = True

    def transform_multimodal_features(self, numerical_df: pd.DataFrame, text_notes: List[str]) -> np.ndarray:
        """
        Concatenates numerical time-series feature array with TF-IDF clinical document text embedding.
        """
        num_arr = numerical_df.values
        
        if not text_notes or not self.is_fit:
            text_arr = np.zeros((len(numerical_df), self.max_text_features))
        else:
            text_arr = self.vectorizer.transform(text_notes).toarray()
            
        return np.hstack([num_arr, text_arr])
