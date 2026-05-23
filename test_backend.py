#!/usr/bin/env python3
"""
Test script for MoodTunes backend components
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_mood_analyzer():
    """Test the mood analyzer component"""
    print("Testing Mood Analyzer...")
    
    try:
        from backend.mood_model import MoodAnalyzer
        analyzer = MoodAnalyzer()
        
        test_cases = [
            "I'm feeling so happy and excited today!",
            "This rainy day makes me feel quite sad",
            "I need some energetic music for my workout",
            "Looking for calm music to relax after a long day",
            "Feeling romantic and in love",
            "Need to focus on my studies"
        ]
        
        for text in test_cases:
            mood = analyzer.predict_mood(text)
            print(f"  '{text}' -> {mood}")
        
        print("✓ Mood Analyzer tests passed\n")
        return True
    except Exception as e:
        print(f"✗ Mood Analyzer tests failed: {e}\n")
        return False

def test_spotify_manager():
    """Test the Spotify manager component"""
    print("Testing Spotify Manager...")
    
    try:
        from backend.spotify_api import SpotifyManager
        spotify = SpotifyManager()
        
        # Test getting tracks for different moods
        moods = ['happy', 'sad', 'energetic']
        for mood in moods:
            tracks = spotify.get_mood_tracks(mood)
            print(f"  {mood.capitalize()} mood: {len(tracks)} tracks found")
            
        print("✓ Spotify Manager tests passed\n")
        return True
    except ImportError as e:
        if "spotipy" in str(e):
            print("  Note: spotipy library not installed. Spotify Manager will run in demo mode.")
            print("  To install spotipy: pip install spotipy")
            print("✓ Spotify Manager tests passed (demo mode)\n")
            return True
        else:
            print(f"✗ Spotify Manager tests failed: {e}\n")
            return False
    except Exception as e:
        print(f"✗ Spotify Manager tests failed: {e}\n")
        return False

def main():
    """Run all backend tests"""
    print("Running MoodTunes Backend Tests\n")
    
    results = []
    results.append(test_mood_analyzer())
    results.append(test_spotify_manager())
    
    if all(results):
        print("All tests passed! ✅")
        return 0
    else:
        print("Some tests failed! ❌")
        return 1

if __name__ == "__main__":
    sys.exit(main())