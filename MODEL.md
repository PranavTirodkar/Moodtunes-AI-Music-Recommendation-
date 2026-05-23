# MoodTunes AI Model Documentation

## Overview

The MoodTunes application uses AI to analyze user input and recommend music based on mood. The current implementation uses a rule-based approach for mood detection, but can be extended with a machine learning model using TensorFlow.

## Current Implementation

The current [mood_model.py](file:///d:/pranav/AI%20powered%20music%20recommendation%20based%20on%20mood/backend/mood_model.py) file uses a simple rule-based approach that matches keywords in the user's text input to predefined mood categories. This approach is lightweight and doesn't require any machine learning dependencies.

## Extending with TensorFlow

To implement a more sophisticated mood detection model, follow these steps:

### 1. Install TensorFlow

```bash
pip install tensorflow
```

### 2. Prepare Training Data

Create a dataset with text samples and corresponding mood labels. You'll need thousands of examples for good results.

### 3. Train the Model

Use the [train_model.py](file:///d:/pranav/AI%20powered%20music%20recommendation%20based%20on%20mood/backend/train_model.py) script to train a neural network on your dataset:

```bash
python backend/train_model.py
```

### 4. Update the MoodAnalyzer Class

Modify the [mood_model.py](file:///d:/pranav/AI%20powered%20music%20recommendation%20based%20on%20mood/backend/mood_model.py) file to load and use the trained TensorFlow model:

```python
# Add these imports at the top
import tensorflow as tf
from tensorflow.keras.models import load_model

# In the __init__ method, load the trained model
def __init__(self, model_path='mood_classifier.h5'):
    if os.path.exists(model_path):
        try:
            self.model = load_model(model_path)
            # Load tokenizer and label encoder
            with open('tokenizer.pickle', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            with open('label_encoder.pickle', 'rb') as handle:
                self.label_encoder = pickle.load(handle)
            self.use_ml_model = True
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.use_ml_model = False
            self._init_rule_based_model()
    else:
        self.use_ml_model = False
        self._init_rule_based_model()

# Add a method to predict using the ML model
def _predict_with_ml_model(self, text):
    # Preprocess text
    sequence = self.tokenizer.texts_to_sequences([text])
    padded_sequence = tf.keras.utils.pad_sequences(sequence, maxlen=50, padding='post')
    
    # Predict
    prediction = self.model.predict(padded_sequence)
    predicted_class = np.argmax(prediction, axis=1)[0]
    mood = self.label_encoder.inverse_transform([predicted_class])[0]
    
    return mood
```

### 5. Model Architecture

The example training script creates a neural network with:
- An embedding layer to convert text to numerical vectors
- An LSTM layer to process sequential text data
- Dense layers for classification
- Dropout for regularization

### 6. Improving the Model

Consider these enhancements:
- Use pre-trained embeddings like Word2Vec or GloVe
- Implement attention mechanisms
- Use transformer models like BERT for better text understanding
- Collect more diverse training data
- Implement data augmentation techniques

## Mood Categories

The current implementation supports 6 mood categories:
1. Happy
2. Sad
3. Energetic
4. Calm
5. Romantic
6. Focused

You can extend this by adding more categories to the training data and updating the model accordingly.

## Integration with Frontend

The frontend sends user input to the backend via the `/api/mood` endpoint. The backend analyzes the text and returns the detected mood, which is then used to fetch music recommendations from Spotify.

## Performance Considerations

- The rule-based approach is fast and lightweight
- TensorFlow models may require more computational resources
- Consider caching predictions for common inputs
- Implement rate limiting to prevent abuse