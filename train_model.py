#!/usr/bin/env python3
"""
MoodTunes AI Model Training Script

This script demonstrates how to train a TensorFlow model for mood classification
based on text input. In a production environment, you would use a larger dataset
with labeled examples of text and corresponding moods.

For demonstration purposes, we'll create a synthetic dataset.
"""

# Static analysis comments to suppress import warnings
# pylint: disable=import-error
# pyright: reportMissingImports=false

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import json
import os
import random

# Direct imports for TensorFlow/Keras - these work at runtime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def create_enhanced_sample_dataset():
    """Create an enhanced sample dataset for mood classification with more varied examples"""
    # Enhanced data with more examples for better training
    data = [
        # Happy mood examples
        ("I feel so happy today!", "happy"),
        ("What a wonderful day!", "happy"),
        ("I'm excited about the weekend", "happy"),
        ("Life is good", "happy"),
        ("I'm smiling all day", "happy"),
        ("This makes me so joyful", "happy"),
        ("I'm thrilled with the results", "happy"),
        ("Feeling optimistic and cheerful", "happy"),
        ("What a fantastic experience", "happy"),
        ("I'm over the moon!", "happy"),
        ("This is absolutely amazing", "happy"),
        ("I'm bursting with happiness", "happy"),
        ("So delighted and pleased", "happy"),
        ("I'm in a great mood today", "happy"),
        ("Feeling blessed and grateful", "happy"),
        
        # Sad mood examples
        ("I feel so sad and lonely", "sad"),
        ("Today is a terrible day", "sad"),
        ("I'm feeling depressed", "sad"),
        ("Everything is going wrong", "sad"),
        ("I miss my friends", "sad"),
        ("This is heartbreaking", "sad"),
        ("I'm feeling down in the dumps", "sad"),
        ("Such a gloomy and dreary day", "sad"),
        ("I'm overwhelmed with sorrow", "sad"),
        ("Feeling blue and melancholy", "sad"),
        ("This is making me feel miserable", "sad"),
        ("I'm struggling with sadness", "sad"),
        ("Feeling hopeless and defeated", "sad"),
        ("My heart is heavy today", "sad"),
        ("I'm drowning in despair", "sad"),
        
        # Energetic mood examples
        ("I'm ready to conquer the world!", "energetic"),
        ("Let's go for a run!", "energetic"),
        ("I need some high energy music", "energetic"),
        ("Feeling pumped up", "energetic"),
        ("Ready for adventure", "energetic"),
        ("I'm fired up and ready to go", "energetic"),
        ("Let's get this party started", "energetic"),
        ("Feeling alive and vibrant", "energetic"),
        ("I'm bursting with energy", "energetic"),
        ("Time to get moving", "energetic"),
        ("I'm charged up and motivated", "energetic"),
        ("Let's make some noise", "energetic"),
        ("Feeling dynamic and powerful", "energetic"),
        ("I'm ready to take on anything", "energetic"),
        ("Time to unleash my potential", "energetic"),
        
        # Calm mood examples
        ("I just want to relax", "calm"),
        ("Peaceful moments by the lake", "calm"),
        ("Meditation time", "calm"),
        ("Quiet and serene", "calm"),
        ("Looking for something soothing", "calm"),
        ("I need some tranquility", "calm"),
        ("Feeling zen and peaceful", "calm"),
        ("Let's find some serenity", "calm"),
        ("Time for some quiet reflection", "calm"),
        ("I'm seeking inner peace", "calm"),
        ("Need to decompress and unwind", "calm"),
        ("Feeling mellow and relaxed", "calm"),
        ("Let's enjoy some stillness", "calm"),
        ("Time for gentle contemplation", "calm"),
        ("Looking for peaceful vibes", "calm"),
        
        # Romantic mood examples
        ("Thinking of my loved one", "romantic"),
        ("Beautiful sunset with my partner", "romantic"),
        ("Love is in the air", "romantic"),
        ("Romantic evening planned", "romantic"),
        ("Feeling affectionate", "romantic"),
        ("My heart is full of love", "romantic"),
        ("This is such a tender moment", "romantic"),
        ("Feeling deeply connected", "romantic"),
        ("So in love and devoted", "romantic"),
        ("This is pure romance", "romantic"),
        ("Feeling passionate and intimate", "romantic"),
        ("My soulmate and I together", "romantic"),
        ("This is a magical love story", "romantic"),
        ("Feeling cherished and adored", "romantic"),
        ("Our love is blossoming", "romantic"),
        
        # Focused mood examples
        ("Time to study", "focused"),
        ("Need to concentrate on work", "focused"),
        ("Deep focus session", "focused"),
        ("Programming mode activated", "focused"),
        ("Research time", "focused"),
        ("Let's get into the zone", "focused"),
        ("Time for deep work", "focused"),
        ("Need to lock in and focus", "focused"),
        ("Let's sharpen the mind", "focused"),
        ("Time for serious concentration", "focused"),
        ("Entering productivity mode", "focused"),
        ("Need to eliminate distractions", "focused"),
        ("Time for mindful attention", "focused"),
        ("Let's achieve peak focus", "focused"),
        ("Ready for intensive work", "focused"),
    ]
    
    texts, labels = zip(*data)
    return list(texts), list(labels)

def load_spotify_datasets():
    """Load and process Spotify datasets to create mood-labeled training data"""
    combined_features = []
    combined_labels = []
    
    # Process the first dataset
    try:
        df1 = pd.read_csv('../Music Recommendation System using Spotify Dataset.csv')
        print(f"Loaded first dataset with {len(df1)} records")
        
        # Take a sample to avoid too much data and improve training speed
        df1_sample = df1.sample(n=min(10000, len(df1)), random_state=42)
        
        # Create mood labels based on audio features
        # This is a simplified approach - in practice, you would have actual mood labels
        for _, row in df1_sample.iterrows():
            # Simple heuristic to assign moods based on audio features
            valence = row['valence']
            energy = row['energy']
            danceability = row['danceability']
            
            # Assign mood based on combination of features
            if valence > 0.7 and energy > 0.7:
                mood = 'happy'
            elif valence < 0.3 and energy < 0.3:
                mood = 'sad'
            elif energy > 0.7 and danceability > 0.7:
                mood = 'energetic'
            elif energy < 0.3 and valence > 0.4:
                mood = 'calm'
            elif valence > 0.5 and danceability > 0.5:
                mood = 'romantic'
            else:
                mood = 'focused'
                
            # Create a text-like representation from audio features
            text_repr = f"valence:{valence},energy:{energy},danceability:{danceability},acousticness:{row['acousticness']},instrumentalness:{row['instrumentalness']}"
            combined_features.append(text_repr)
            combined_labels.append(mood)
            
        print(f"Processed {len(combined_features)} samples from first dataset")
    except Exception as e:
        print(f"Error processing first dataset: {e}")
    
    # Process the second dataset
    try:
        df2 = pd.read_csv('../Music Recommendation System using Spotify New Dataset.csv')
        print(f"Loaded second dataset with {len(df2)} records")
        
        # Take a sample to avoid too much data
        df2_sample = df2.sample(n=min(5000, len(df2)), random_state=42)
        
        # Create mood labels based on audio features
        for _, row in df2_sample.iterrows():
            # Simple heuristic to assign moods based on audio features
            valence = row['valence']
            energy = row['energy']
            danceability = row['danceability']
            
            # Assign mood based on combination of features
            if valence > 0.7 and energy > 0.7:
                mood = 'happy'
            elif valence < 0.3 and energy < 0.3:
                mood = 'sad'
            elif energy > 0.7 and danceability > 0.7:
                mood = 'energetic'
            elif energy < 0.3 and valence > 0.4:
                mood = 'calm'
            elif valence > 0.5 and danceability > 0.5:
                mood = 'romantic'
            else:
                mood = 'focused'
                
            # Create a text-like representation from audio features
            text_repr = f"valence:{valence},energy:{energy},danceability:{danceability},acousticness:{row['acousticness']},instrumentalness:{row['instrumentalness']}"
            combined_features.append(text_repr)
            combined_labels.append(mood)
            
        print(f"Processed {len(combined_features)} total samples")
    except Exception as e:
        print(f"Error processing second dataset: {e}")
    
    return combined_features, combined_labels

def preprocess_data(texts, labels, max_words=2000, max_len=100):
    """Preprocess text data for training"""
    # Tokenize texts
    tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
    
    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    
    return padded_sequences, encoded_labels, tokenizer, label_encoder

def create_enhanced_model(vocab_size, embedding_dim=128, max_length=100, num_classes=6):
    """Create an enhanced neural network model for mood classification"""
    model = Sequential([
        Embedding(vocab_size, embedding_dim, input_length=max_length),
        LSTM(128, dropout=0.2, recurrent_dropout=0.2, return_sequences=True),
        LSTM(64, dropout=0.2, recurrent_dropout=0.2),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    
    return model

def train_mood_model():
    """Train the mood classification model"""
    print("Loading Spotify datasets...")
    spotify_texts, spotify_labels = load_spotify_datasets()
    
    print("Creating enhanced sample dataset...")
    sample_texts, sample_labels = create_enhanced_sample_dataset()
    
    # Combine both datasets
    print("Combining datasets...")
    all_texts = sample_texts + spotify_texts
    all_labels = sample_labels + spotify_labels
    
    print(f"Total training samples: {len(all_texts)}")
    
    print("Preprocessing data...")
    X, y, tokenizer, label_encoder = preprocess_data(all_texts, all_labels, max_words=2000, max_len=100)
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Creating model...")
    vocab_size = len(tokenizer.word_index) + 1 if hasattr(tokenizer, 'word_index') and tokenizer.word_index else 2000
    
    # Safely get the number of classes
    if hasattr(label_encoder, 'classes_') and label_encoder.classes_ is not None:
        num_classes = len(label_encoder.classes_)
    else:
        # Fallback: count unique labels
        num_classes = len(np.unique(y)) if isinstance(y, (list, np.ndarray)) else 6
    
    model = create_enhanced_model(vocab_size, num_classes=num_classes)
    
    print("Model architecture:")
    model.summary()
    
    print("Training model...")
    # Train for more epochs with validation split
    history = model.fit(
        X_train, y_train,
        epochs=15,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    print("Training completed!")
    print(f"Final accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    # Save the model and preprocessing tools
    print("Saving model and preprocessing tools...")
    model.save('mood_classifier.h5')
    
    # Save tokenizer and label encoder for later use
    import pickle
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('label_encoder.pickle', 'wb') as handle:
        pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("Model and tools saved successfully!")
    if hasattr(label_encoder, 'classes_') and label_encoder.classes_ is not None:
        print(f"Mood classes: {label_encoder.classes_}")

if __name__ == "__main__":
    train_mood_model()