import pandas as pd
import random
import os

class DatasetIntegrator:
    def __init__(self):
        """Initialize the dataset integrator"""
        self.mood_mapping = {
            'happy': ['Happy song', 'Joyful song', 'Upbeat song'],
            'sad': ['Sad song', 'Melancholic song', 'Depressing song'],
            'energetic': ['Energetic song', 'High-energy song', 'Intense song'],
            'calm': ['Calm song', 'Peaceful song', 'Relaxing song'],
            'romantic': ['Romantic song', 'Love song', 'Intimate song'],
            'focused': ['Focus song', 'Study music', 'Concentration music']
        }
    
    def load_datasets(self):
        """Load the Spotify datasets"""
        try:
            # Load both datasets with full paths
            dataset1_path = os.path.join('..', 'Music Recommendation System using Spotify Dataset.csv')
            dataset2_path = os.path.join('..', 'Music Recommendation System using Spotify New Dataset.csv')
            
            print(f"Looking for dataset 1 at: {dataset1_path}")
            print(f"Looking for dataset 2 at: {dataset2_path}")
            
            if os.path.exists(dataset1_path):
                df1 = pd.read_csv(dataset1_path)
                print(f"Loaded dataset 1 with {len(df1)} records")
            else:
                print(f"Dataset 1 not found at {dataset1_path}")
                df1 = pd.DataFrame()
                
            if os.path.exists(dataset2_path):
                df2 = pd.read_csv(dataset2_path)
                print(f"Loaded dataset 2 with {len(df2)} records")
            else:
                print(f"Dataset 2 not found at {dataset2_path}")
                df2 = pd.DataFrame()
                
            return df1, df2
        except Exception as e:
            print(f"Error loading datasets: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    def categorize_by_mood(self, df):
        """Categorize songs by mood based on valence and other features"""
        mood_songs = {
            'happy': [],
            'sad': [],
            'energetic': [],
            'calm': [],
            'romantic': [],
            'focused': []
        }
        
        if df.empty:
            return mood_songs
            
        for _, row in df.iterrows():
            try:
                # Handle potential missing or NaN values
                valence = float(row.get('valence', 0.5) or 0.5)
                energy = float(row.get('energy', 0.5) or 0.5)
                danceability = float(row.get('danceability', 0.5) or 0.5)
                
                # Simple heuristic to assign moods based on audio features
                if valence > 0.7 and energy > 0.5:
                    mood_songs['happy'].append(row)
                elif valence < 0.3 and energy < 0.4:
                    mood_songs['sad'].append(row)
                elif energy > 0.7 and danceability > 0.7:
                    mood_songs['energetic'].append(row)
                elif energy < 0.3 and valence > 0.4:
                    mood_songs['calm'].append(row)
                elif valence > 0.5 and danceability > 0.5:
                    mood_songs['romantic'].append(row)
                else:
                    mood_songs['focused'].append(row)
            except Exception as e:
                # Skip rows with issues
                continue
                
        return mood_songs
    
    def create_track_dict(self, row, track_id):
        """Convert a dataset row to a track dictionary"""
        try:
            # Handle potential list-like strings in artists column
            artists = row.get('artists', 'Unknown Artist')
            if isinstance(artists, str) and artists.startswith('[') and artists.endswith(']'):
                # Parse the list-like string
                try:
                    import ast
                    artist_list = ast.literal_eval(artists)
                    artist = artist_list[0] if artist_list else 'Unknown Artist'
                except:
                    artist = 'Unknown Artist'
            else:
                artist = artists if pd.notna(artists) else 'Unknown Artist'
            
            # Get other fields with fallbacks
            name = row.get('name', f'Unknown Track {track_id}')
            album = row.get('album', 'Unknown Album')
            duration_ms = row.get('duration_ms', 180000)  # Default to 3 minutes
            popularity = row.get('popularity', 0)
            
            # Convert duration to MM:SS format
            duration_seconds = int(duration_ms) // 1000
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            duration = f"{minutes}:{seconds:02d}"
            
            # Create a simple placeholder album art
            album_art = f"https://placehold.co/300x300/{random.choice(['8a2be2', 'ff6b6b', '4e54c8', '20b2aa', 'da70d6'])}/ffffff?text={str(name)[:10].replace(' ', '+')}"
            
            return {
                'id': track_id,
                'title': name if pd.notna(name) else f'Unknown Track {track_id}',
                'artist': artist,
                'album': album if pd.notna(album) else 'Unknown Album',
                'duration': duration,
                'albumArt': album_art,
                'previewUrl': f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{random.randint(1, 50)}.mp3",
                'uri': f"spotify:track:{track_id}"
            }
        except Exception as e:
            print(f"Error creating track dict: {e}")
            return None
    
    def integrate_datasets(self):
        """Main method to integrate datasets and return mood-based tracks"""
        # Load datasets
        df1, df2 = self.load_datasets()
        
        # Combine datasets
        if not df1.empty and not df2.empty:
            combined_df = pd.concat([df1, df2], ignore_index=True)
        elif not df1.empty:
            combined_df = df1
        elif not df2.empty:
            combined_df = df2
        else:
            print("No datasets found to integrate")
            return {}
        
        print(f"Combined dataset has {len(combined_df)} records")
        
        # Take a sample to avoid too much data (adjust as needed)
        sample_size = min(5000, len(combined_df))
        df_sample = combined_df.sample(n=sample_size, random_state=42)
        
        # Categorize songs by mood
        mood_songs = self.categorize_by_mood(df_sample)
        
        # Convert to track dictionaries
        mood_tracks = {}
        for mood, songs in mood_songs.items():
            tracks = []
            for i, song in enumerate(songs[:50]):  # Limit to 50 songs per mood
                track = self.create_track_dict(song, f"{mood}_{i+1}")
                if track:
                    tracks.append(track)
            mood_tracks[mood] = tracks
            print(f"Processed {len(tracks)} {mood} tracks")
        
        return mood_tracks

def update_demo_tracks():
    """Update the demo tracks in spotify_api.py with dataset tracks"""
    # Initialize the integrator
    integrator = DatasetIntegrator()
    
    # Get mood-based tracks from datasets
    dataset_tracks = integrator.integrate_datasets()
    
    if not dataset_tracks:
        print("No tracks from datasets to integrate")
        return
    
    # Read the current spotify_api.py file
    spotify_api_path = 'spotify_api.py'
    try:
        with open(spotify_api_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading spotify_api.py: {e}")
        return
    
    # Find the demo_tracks_data section
    start_marker = "demo_tracks_data = {"
    end_marker = "        }"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find demo_tracks_data section")
        return
    
    # Find the end of the demo_tracks_data section
    # We need to find the closing brace that ends the dictionary
    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        print("Could not find end of demo_tracks_data section")
        return
    
    # Adjust end_idx to include the closing brace and newline
    end_idx = content.find("\n", end_idx) + 1
    
    # Extract the part before and after the demo_tracks_data section
    before_section = content[:start_idx + len(start_marker)]
    after_section = content[end_idx:]
    
    # Generate the new demo_tracks_data section
    new_section = "\n"
    for mood in ['happy', 'sad', 'energetic', 'calm', 'romantic', 'focused']:
        new_section += f"            '{mood}': [\n"
        # Add dataset tracks (up to 8 per mood)
        tracks = dataset_tracks.get(mood, [])
        for track in tracks[:8]:  # Limit to 8 tracks per mood from dataset
            new_section += f"                {{\n"
            new_section += f"                    'id': '{track['id']}',\n"
            new_section += f"                    'title': \"{track['title']}\",\n"
            new_section += f"                    'artist': \"{track['artist']}\",\n"
            new_section += f"                    'album': \"{track['album']}\",\n"
            new_section += f"                    'duration': \"{track['duration']}\",\n"
            new_section += f"                    'albumArt': \"{track['albumArt']}\",\n"
            new_section += f"                    'previewUrl': \"{track['previewUrl']}\",\n"
            new_section += f"                    'uri': \"{track['uri']}\"\n"
            new_section += f"                }},\n"
        new_section += f"            ],\n"
    
    # Combine everything
    new_content = before_section + new_section + "        }" + after_section
    
    # Write back to the file
    try:
        with open(spotify_api_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated spotify_api.py with dataset tracks")
    except Exception as e:
        print(f"Error writing to spotify_api.py: {e}")

if __name__ == "__main__":
    # Run the integration
    update_demo_tracks()