from spotify_api import SpotifyManager

# Test the updated SpotifyManager with more songs
if __name__ == "__main__":
    # Initialize the SpotifyManager
    spotify_manager = SpotifyManager()
    
    # Test getting tracks for different moods
    moods = ['happy', 'sad', 'energetic', 'calm', 'romantic', 'focused']
    
    for mood in moods:
        print(f"\n--- {mood.capitalize()} Tracks ---")
        tracks = spotify_manager.get_mood_tracks(mood)
        print(f"Found {len(tracks)} tracks for {mood} mood:")
        for i, track in enumerate(tracks, 1):
            print(f"  {i}. {track['title']} by {track['artist']}")