# MoodTunes - AI Powered Music Recommendation Based on Mood

A modern web application that recommends music based on your current mood using AI technology.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with TensorFlow for AI mood analysis
- **Music API**: Spotify Web API
- **Deployment**: Flask (Python web framework)

## Project Structure

```
.
├── index.html          # Main HTML file
├── styles.css          # Styling for the application
├── script.js           # Client-side JavaScript for interactivity
├── backend/            # Python backend with AI model
│   ├── app.py          # Flask application
│   ├── mood_model.py   # TensorFlow model for mood analysis
│   ├── spotify_api.py  # Spotify API integration
│   ├── train_model.py  # Model training script
│   ├── MODEL.md        # Model documentation
│   ├── .env.example    # Example environment variables
│   └── requirements.txt # Python dependencies
├── test_backend.py     # Backend component tests
└── README.md           # This file
```

## Features

1. **Modern UI**: Clean, responsive design with gradient accents
2. **Mood Selection**: Choose from predefined moods or describe your feelings
3. **AI Analysis**: TensorFlow model analyzes text input to detect mood
4. **Spotify Integration**: Fetches and displays relevant music recommendations
5. **Responsive Design**: Works on mobile, tablet, and desktop devices
6. **Expanded Song Database**: Over 60 songs across 6 mood categories

## Setup Instructions

### Frontend

The frontend is ready to use. Simply open `index.html` in a web browser.

### Backend Setup

1. Install Python 3.7+
2. Create a virtual environment:
   ```bash
   python -m venv moodtunes-env
   source moodtunes-env/bin/activate  # On Windows: moodtunes-env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Set up Spotify Developer Account:
   - Go to https://developer.spotify.com/dashboard/
   - Create a new app
   - Get your Client ID and Client Secret
   - Add `http://localhost:5000/callback` as a redirect URI

5. Create a `.env` file in the backend directory based on `.env.example`:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Then edit the `.env` file and add your Spotify credentials

6. Run the Flask application:
   ```bash
   python backend/app.py
   ```

7. Visit `http://localhost:5000` in your browser

### Running Tests

To test the backend components:

```bash
python test_backend.py
```

## How It Works

1. **Mood Detection**:
   - Predefined moods map to specific music genres
   - Custom mood descriptions are analyzed by our TensorFlow model
   - Model uses Natural Language Processing to classify emotional sentiment

2. **Music Recommendation**:
   - Spotify API is queried with mood-specific parameters
   - Results are filtered and sorted based on popularity and relevance
   - Album art and track information are displayed
   - Expanded demo database with over 60 songs across 6 moods

3. **Playback**:
   - Integration with Spotify Web Playback SDK
   - Users can play tracks directly in the browser (requires Spotify Premium)

## AI Model Development

The application includes scripts and documentation for training your own mood detection model:

1. Use [train_model.py](file:///d:/pranav/AI%20powered%20music%20recommendation%20based%20on%20mood/backend/train_model.py) to train a TensorFlow model
2. Refer to [MODEL.md](file:///d:/pranav/AI%20powered%20music%20recommendation%20based%20on%20mood/backend/MODEL.md) for detailed documentation
3. Extend the model with more sophisticated NLP techniques

## Song Database Expansion

The demo mode now includes an expanded song database with over 60 songs across 6 mood categories:
- Happy: 12 songs
- Sad: 10 songs
- Energetic: 10 songs
- Calm: 8 songs
- Romantic: 10 songs
- Focused: 10 songs

Refer to [HOW_TO_ADD_MORE_SONGS.md](file:///d:/pranav/AI%20powered%20music%20recommendation%20based%20on%20mood/HOW_TO_ADD_MORE_SONGS.md) for instructions on adding more songs.

## Future Enhancements

- [ ] Train a more sophisticated mood detection model
- [ ] Add user accounts and preference tracking
- [ ] Implement collaborative filtering for better recommendations
- [ ] Add audio analysis for real-time mood detection
- [ ] Integrate with other music services (Apple Music, YouTube Music)
- [ ] Automatically process Spotify datasets for dynamic song database

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.