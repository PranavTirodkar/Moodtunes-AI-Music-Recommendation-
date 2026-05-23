import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from mood_model import MoodAnalyzer
from spotify_api import SpotifyManager

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='..', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Initialize services
mood_analyzer = MoodAnalyzer()
spotify_manager = SpotifyManager()

@app.route('/')
def index():
    """Serve the main frontend application"""
    return app.send_static_file('index.html')

@app.route('/api/mood', methods=['POST'])
def analyze_mood():
    """Analyze text input to determine mood"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        mood = mood_analyzer.predict_mood(text)
        return jsonify({'mood': mood})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/<mood>')
def get_recommendations(mood):
    """Get music recommendations for a specific mood"""
    try:
        tracks = spotify_manager.get_mood_tracks(mood)
        return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playback/<track_id>')
def get_track_uri(track_id):
    """Get Spotify URI for a track to enable playback"""
    try:
        uri = spotify_manager.get_track_uri(track_id)
        return jsonify({'uri': uri})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)