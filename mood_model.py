import numpy as np
import pickle
import os

# Static analysis comments to suppress import warnings
# pylint: disable=import-error
# pyright: reportMissingImports=false

# Direct imports for TensorFlow/Keras - these work at runtime
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

class MoodAnalyzer:
    def __init__(self, model_path='mood_classifier.h5'):
        """Initialize the mood analyzer with a trained TensorFlow model"""
        self.moods = ['happy', 'sad', 'energetic', 'calm', 'romantic', 'focused']
        
        # Try to load the trained model
        if os.path.exists(model_path):
            try:
                self.model = load_model(model_path)
                # Load tokenizer and label encoder
                with open('tokenizer.pickle', 'rb') as handle:
                    self.tokenizer = pickle.load(handle)
                with open('label_encoder.pickle', 'rb') as handle:
                    self.label_encoder = pickle.load(handle)
                self.use_ml_model = True
                print("Successfully loaded trained TensorFlow model")
            except Exception as e:
                print(f"Failed to load model: {e}")
                self.use_ml_model = False
                self._init_rule_based_model()
        else:
            print("Trained model not found, using rule-based model")
            self.use_ml_model = False
            self._init_rule_based_model()
    
    def _init_rule_based_model(self):
        """Initialize the rule-based model for demonstration"""
        # Create a simple rule-based model for demonstration
        self.mood_keywords = {
            'happy': ['happy', 'joy', 'excited', 'cheerful', 'delighted', 'pleased', 'glad', 'content'],
            'sad': ['sad', 'depressed', 'unhappy', 'miserable', 'gloomy', 'melancholy', 'down', 'blue'],
            'energetic': ['energetic', 'active', 'lively', 'vigorous', 'dynamic', 'vibrant', 'pumped', 'hyped'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'quiet', 'still', 'mellow'],
            'romantic': ['romantic', 'love', 'affectionate', 'passionate', 'intimate', 'tender', 'sweet', 'heart'],
            'focused': ['focused', 'concentrated', 'attentive', 'alert', 'mindful', 'productive', 'studious', 'thoughtful']
        }
    
    def _predict_with_ml_model(self, text):
        """Predict mood using the trained ML model"""
        try:
            # Preprocess text
            sequence = self.tokenizer.texts_to_sequences([text])
            padded_sequence = pad_sequences(sequence, maxlen=50, padding='post')
            
            # Predict
            prediction = self.model.predict(padded_sequence)
            predicted_class = np.argmax(prediction, axis=1)[0]
            mood = self.label_encoder.inverse_transform([predicted_class])[0]
            
            return mood
        except Exception as e:
            print(f"Error in ML prediction: {e}")
            # Fallback to rule-based model
            return self.predict_mood_rule_based(text)
    
    def predict_mood_rule_based(self, text):
        """
        Predict the mood of a given text using rule-based approach
        
        Args:
            text (str): The text to analyze
            
        Returns:
            str: The predicted mood
        """
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Count keyword matches for each mood
        mood_scores = {}
        for mood, keywords in self.mood_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            mood_scores[mood] = score
        
        # Return the mood with the highest score, or default to 'happy'
        if max(mood_scores.values()) > 0:
            # Convert to list to avoid type issues
            items = list(mood_scores.items())
            return max(items, key=lambda x: x[1])[0]
        else:
            # If no keywords match, return a random mood or default
            return 'happy'
    
    def predict_mood(self, text):
        """
        Predict the mood of a given text using either ML model or rule-based approach
        
        Args:
            text (str): The text to analyze
            
        Returns:
            str: The predicted mood
        """
        if self.use_ml_model:
            return self._predict_with_ml_model(text)
        else:
            return self.predict_mood_rule_based(text)
    
    def train_model(self, texts, labels):
        """
        Train the mood analysis model (placeholder for actual implementation)
        
        Args:
            texts (list): List of text samples
            labels (list): List of corresponding mood labels
        """
        # In a real implementation with TensorFlow, you would:
        # 1. Preprocess the text data
        # 2. Vectorize the text using TF-IDF or embeddings
        # 3. Train a neural network using TensorFlow
        # 4. Save the trained model
        
        print("Training model with", len(texts), "samples...")
        # This is where you would implement the actual training logic
        # For now, we'll just print a message
        print("Model training completed!")
        
    def save_model(self, filepath):
        """Save the trained model to disk"""
        # In a real implementation, you would save the TensorFlow model
        print(f"Model saved to {filepath}")
        
    def load_model(self, filepath):
        """Load a trained model from disk"""
        # In a real implementation, you would load the TensorFlow model
        print(f"Model loaded from {filepath}")

# Example usage (for testing purposes)
if __name__ == "__main__":
    analyzer = MoodAnalyzer()
    
    # Test the mood prediction
    test_texts = [
        "I'm feeling so happy and excited today!",
        "This rainy day makes me feel quite sad",
        "I need some energetic music for my workout",
        "Looking for calm music to relax after a long day",
        "Feeling romantic and in love",
        "Need to focus on my studies"
    ]
    
    for text in test_texts:
        mood = analyzer.predict_mood(text)
        print(f"Text: '{text}' -> Predicted mood: {mood}")