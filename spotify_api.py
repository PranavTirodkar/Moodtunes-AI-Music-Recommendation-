import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyManager:
    def __init__(self):
        """Initialize Spotify API client"""
        # In production, these should be stored securely in environment variables
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        # For demo purposes, we'll use placeholder values
        # In a real application, you must set these environment variables
        if not client_id or not client_secret or client_id == '' or client_secret == '':
            print("Warning: Spotify credentials not found. Using demo mode.")
            self.demo_mode = True
        else:
            print("Spotify credentials found. Using Spotify API.")
            self.demo_mode = False
            try:
                client_credentials_manager = SpotifyClientCredentials(
                    client_id=client_id, 
                    client_secret=client_secret
                )
                self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                # Test the connection
                self.sp.search(q='test', type='track', limit=1)
                print("Spotify API connection successful.")
            except Exception as e:
                print(f"Error connecting to Spotify API: {e}. Using demo mode.")
                self.demo_mode = True
    
    def get_mood_tracks(self, mood):
        """
        Get music tracks for a specific mood
        
        Args:
            mood (str): The mood to get tracks for
            
        Returns:
            list: List of track dictionaries
        """
        if self.demo_mode:
            return self._get_demo_tracks(mood)
        
        try:
            # Map moods to Spotify search queries with multiple options for variety
            mood_queries = {
                'happy': [
                    'happy upbeat popular',
                    'joyful cheerful music',
                    'feel good songs',
                    'uplifting music',
                    'positive vibe tracks'
                ],
                'sad': [
                    'sad melancholy acoustic',
                    'emotional ballads',
                    'heartfelt songs',
                    'melancholic music',
                    'emotional acoustic'
                ],
                'energetic': [
                    'energetic workout high tempo',
                    'high energy music',
                    'pumped up songs',
                    'motivational tracks',
                    'intense music'
                ],
                'calm': [
                    'calm relaxing ambient',
                    'peaceful meditation music',
                    'soothing instrumental',
                    'relaxing nature sounds',
                    'gentle acoustic'
                ],
                'romantic': [
                    'romantic love songs',
                    'love ballads',
                    'intimate music',
                    'romantic date songs',
                    'couples music'
                ],
                'focused': [
                    'focus concentration instrumental',
                    'study music',
                    'background music for work',
                    'instrumental focus',
                    'productivity music'
                ]
            }
            
            # Select a random query for variety
            queries = mood_queries.get(mood, ['popular'])
            query = random.choice(queries)
            
            # Search for tracks with some randomness in limit
            limit = random.randint(10, 15)
            results = self.sp.search(q=query, type='track', limit=limit)
            
            # Check if results is None or doesn't contain expected structure
            if not results or 'tracks' not in results or 'items' not in results['tracks']:
                print("Warning: Spotify API returned unexpected results structure")
                return self._get_demo_tracks(mood)
            
            tracks = []
            for item in results['tracks']['items']:
                track = {
                    'id': item['id'],
                    'title': item['name'],
                    'artist': item['artists'][0]['name'],
                    'album': item['album']['name'],
                    'duration': self._format_duration(item['duration_ms']),
                    'albumArt': item['album']['images'][0]['url'] if item['album']['images'] else '',
                    'previewUrl': item['preview_url'] if item['preview_url'] else '',
                    'uri': item['uri']  # Add Spotify URI for playback
                }
                tracks.append(track)
            
            # Shuffle tracks for more variety
            random.shuffle(tracks)
            
            return tracks[:12]  # Return up to 12 tracks
        except Exception as e:
            print(f"Error fetching tracks from Spotify: {e}")
            return self._get_demo_tracks(mood)
    
    def _get_demo_tracks(self, mood):
        """Generate demo tracks when Spotify API is not available"""
        # Sample track data for demonstration with preview URLs
        demo_tracks_data = {
            'happy': [
                {
                    'id': 'happy_1',
                    'title': "Good 4 U",
                    'artist': "Olivia Rodrigo",
                    'album': "SOUR",
                    'duration': "2:58",
                    'albumArt': "https://placehold.co/300x300/8a2be2/ffffff?text=Good+4+U",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                    'uri': "spotify:track:happy_1"
                },
                {
                    'id': 'happy_2',
                    'title': "Levitating",
                    'artist': "Dua Lipa",
                    'album': "Future Nostalgia",
                    'duration': "3:23",
                    'albumArt': "https://placehold.co/300x300/ff6b6b/ffffff?text=Levitating",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                    'uri': "spotify:track:happy_2"
                },
                {
                    'id': 'happy_3',
                    'title': "As It Was",
                    'artist': "Harry Styles",
                    'album': "Harry's House",
                    'duration': "2:47",
                    'albumArt': "https://placehold.co/300x300/4e54c8/ffffff?text=As+It+Was",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                    'uri': "spotify:track:happy_3"
                },
                {
                    'id': 'happy_4',
                    'title': "About Damn Time",
                    'artist': "Lizzo",
                    'album': "About Damn Time",
                    'duration': "3:12",
                    'albumArt': "https://placehold.co/300x300/ffa500/ffffff?text=About+Damn+Time",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
                    'uri': "spotify:track:happy_4"
                },
                {
                    'id': 'happy_5',
                    'title': "Running Up That Hill",
                    'artist': "Kate Bush",
                    'album': "Hounds Of Love",
                    'duration': "4:56",
                    'albumArt': "https://placehold.co/300x300/ff1493/ffffff?text=Running+Up+That+Hill",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
                    'uri': "spotify:track:happy_5"
                },
                {
                    'id': 'happy_6',
                    'title': "Uptown Girl",
                    'artist': "Billy Joel",
                    'album': "An Innocent Man",
                    'duration': "3:12",
                    'albumArt': "https://placehold.co/300x300/1e90ff/ffffff?text=Uptown+Girl",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-26.mp3",
                    'uri': "spotify:track:happy_6"
                },
                {
                    'id': 'happy_7',
                    'title': "Shut Up and Dance",
                    'artist': "Walk the Moon",
                    'album': "Walk the Moon",
                    'duration': "3:19",
                    'albumArt': "https://placehold.co/300x300/ff6347/ffffff?text=Shut+Up+and+Dance",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-27.mp3",
                    'uri': "spotify:track:happy_7"
                },
                {
                    'id': 'happy_8',
                    'title': "Can't Stop the Feeling!",
                    'artist': "Justin Timberlake",
                    'album': "Trolls (Original Motion Picture Soundtrack)",
                    'duration': "3:56",
                    'albumArt': "https://placehold.co/300x300/ff1493/ffffff?text=Can't+Stop+the+Feeling",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-28.mp3",
                    'uri': "spotify:track:happy_8"
                },
                {
                    'id': 'happy_9',
                    'title': "Happy",
                    'artist': "Pharrell Williams",
                    'album': "Girl",
                    'duration': "3:53",
                    'albumArt': "https://placehold.co/300x300/FFD700/ffffff?text=Happy",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-29.mp3",
                    'uri': "spotify:track:happy_9"
                },
                {
                    'id': 'happy_10',
                    'title': "Don't Stop Me Now",
                    'artist': "Queen",
                    'album': "Jazz",
                    'duration': "3:29",
                    'albumArt': "https://placehold.co/300x300/FF6347/ffffff?text=Don't+Stop+Me+Now",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-30.mp3",
                    'uri': "spotify:track:happy_10"
                },
                {
                    'id': 'happy_11',
                    'title': "Walking on Sunshine",
                    'artist': "Katrina and the Waves",
                    'album': "Walking on Sunshine",
                    'duration': "3:45",
                    'albumArt': "https://placehold.co/300x300/FFD700/ffffff?text=Walking+on+Sunshine",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-31.mp3",
                    'uri': "spotify:track:happy_11"
                },
                {
                    'id': 'happy_12',
                    'title': "Mr. Blue Sky",
                    'artist': "Electric Light Orchestra",
                    'album': "Out of the Blue",
                    'duration': "5:05",
                    'albumArt': "https://placehold.co/300x300/87CEEB/ffffff?text=Mr.+Blue+Sky",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-32.mp3",
                    'uri': "spotify:track:happy_12"
                }
            ],
            'sad': [
                {
                    'id': 'sad_1',
                    'title': "Someone You Loved",
                    'artist': "Lewis Capaldi",
                    'album': "Divinely Uninspired to a Hellish Extent",
                    'duration': "3:02",
                    'albumArt': "https://placehold.co/300x300/8a2be2/ffffff?text=Someone+You+Loved",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
                    'uri': "spotify:track:sad_1"
                },
                {
                    'id': 'sad_2',
                    'title': "All Too Well",
                    'artist': "Taylor Swift",
                    'album': "Red (Taylor's Version)",
                    'duration': "5:29",
                    'albumArt': "https://placehold.co/300x300/ff6b6b/ffffff?text=All+Too+Well",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
                    'uri': "spotify:track:sad_2"
                },
                {
                    'id': 'sad_3',
                    'title': "Easy On Me",
                    'artist': "Adele",
                    'album': "30",
                    'duration': "3:44",
                    'albumArt': "https://placehold.co/300x300/20b2aa/ffffff?text=Easy+On+Me",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
                    'uri': "spotify:track:sad_3"
                },
                {
                    'id': 'sad_4',
                    'title': "Breathe Me",
                    'artist': "Sia",
                    'album': "Colour the Small One",
                    'duration': "4:34",
                    'albumArt': "https://placehold.co/300x300/da70d6/ffffff?text=Breathe+Me",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
                    'uri': "spotify:track:sad_4"
                },
                {
                    'id': 'sad_5',
                    'title': "Hurt",
                    'artist': "Johnny Cash",
                    'album': "American IV: The Man Comes Around",
                    'duration': "3:38",
                    'albumArt': "https://placehold.co/300x300/2f4f4f/ffffff?text=Hurt",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-29.mp3",
                    'uri': "spotify:track:sad_5"
                },
                {
                    'id': 'sad_6',
                    'title': "Mad World",
                    'artist': "Gary Jules",
                    'album': "Mad World (Single)",
                    'duration': "3:06",
                    'albumArt': "https://placehold.co/300x300/696969/ffffff?text=Mad+World",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-30.mp3",
                    'uri': "spotify:track:sad_6"
                },
                {
                    'id': 'sad_7',
                    'title': "The Night We Met",
                    'artist': "Lord Huron",
                    'album': "Strange Trails",
                    'duration': "3:28",
                    'albumArt': "https://placehold.co/300x300/556b2f/ffffff?text=The+Night+We+Met",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-31.mp3",
                    'uri': "spotify:track:sad_7"
                },
                {
                    'id': 'sad_8',
                    'title': "Someone Like You",
                    'artist': "Adele",
                    'album': "21",
                    'duration': "4:45",
                    'albumArt': "https://placehold.co/300x300/2F4F4F/ffffff?text=Someone+Like+You",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-32.mp3",
                    'uri': "spotify:track:sad_8"
                },
                {
                    'id': 'sad_9',
                    'title': "Fix You",
                    'artist': "Coldplay",
                    'album': "X&Y",
                    'duration': "4:55",
                    'albumArt': "https://placehold.co/300x300/696969/ffffff?text=Fix+You",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-33.mp3",
                    'uri': "spotify:track:sad_9"
                },
                {
                    'id': 'sad_10',
                    'title': "Hallelujah",
                    'artist': "Jeff Buckley",
                    'album': "Grace",
                    'duration': "6:53",
                    'albumArt': "https://placehold.co/300x300/708090/ffffff?text=Hallelujah",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-34.mp3",
                    'uri': "spotify:track:sad_10"
                }
            ],
            'energetic': [
                {
                    'id': 'energetic_1',
                    'title': "Thunder",
                    'artist': "Imagine Dragons",
                    'album': "Evolve",
                    'duration': "3:07",
                    'albumArt': "https://placehold.co/300x300/8a2be2/ffffff?text=Thunder",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
                    'uri': "spotify:track:energetic_1"
                },
                {
                    'id': 'energetic_2',
                    'title': "Stronger",
                    'artist': "Kanye West",
                    'album': "Graduation",
                    'duration': "5:12",
                    'albumArt': "https://placehold.co/300x300/ff6b6b/ffffff?text=Stronger",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
                    'uri': "spotify:track:energetic_2"
                },
                {
                    'id': 'energetic_3',
                    'title': "Uptown Funk",
                    'artist': "Mark Ronson ft. Bruno Mars",
                    'album': "Uptown Special",
                    'duration': "4:30",
                    'albumArt': "https://placehold.co/300x300/ffd700/ffffff?text=Uptown+Funk",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3",
                    'uri': "spotify:track:energetic_3"
                },
                {
                    'id': 'energetic_4',
                    'title': "Can't Stop the Feeling!",
                    'artist': "Justin Timberlake",
                    'album': "Trolls (Original Motion Picture Soundtrack)",
                    'duration': "3:56",
                    'albumArt': "https://placehold.co/300x300/ff4500/ffffff?text=Can't+Stop+the+Feeling",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3",
                    'uri': "spotify:track:energetic_4"
                },
                {
                    'id': 'energetic_5',
                    'title': "Uptown Funk",
                    'artist': "Mark Ronson ft. Bruno Mars",
                    'album': "Uptown Special",
                    'duration': "4:30",
                    'albumArt': "https://placehold.co/300x300/FF4500/ffffff?text=Uptown+Funk",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-35.mp3",
                    'uri': "spotify:track:energetic_5"
                },
                {
                    'id': 'energetic_6',
                    'title': "Shut Up and Dance",
                    'artist': "Walk the Moon",
                    'album': "Walk the Moon",
                    'duration': "3:19",
                    'albumArt': "https://placehold.co/300x300/FF6347/ffffff?text=Shut+Up+and+Dance",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-36.mp3",
                    'uri': "spotify:track:energetic_6"
                },
                {
                    'id': 'energetic_7',
                    'title': "Don't Stop Me Now",
                    'artist': "Queen",
                    'album': "Jazz",
                    'duration': "3:29",
                    'albumArt': "https://placehold.co/300x300/FFD700/ffffff?text=Don't+Stop+Me+Now",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-37.mp3",
                    'uri': "spotify:track:energetic_7"
                },
                {
                    'id': 'energetic_8',
                    'title': "Mr. Brightside",
                    'artist': "The Killers",
                    'album': "Hot Fuss",
                    'duration': "3:42",
                    'albumArt': "https://placehold.co/300x300/FF6347/ffffff?text=Mr.+Brightside",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-38.mp3",
                    'uri': "spotify:track:energetic_8"
                },
                {
                    'id': 'energetic_9',
                    'title': "Dance Monkey",
                    'artist': "Tones and I",
                    'album': "The Kids Are Coming",
                    'duration': "3:29",
                    'albumArt': "https://placehold.co/300x300/FFD700/ffffff?text=Dance+Monkey",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-39.mp3",
                    'uri': "spotify:track:energetic_9"
                },
                {
                    'id': 'energetic_10',
                    'title': "Blinding Lights",
                    'artist': "The Weeknd",
                    'album': "After Hours",
                    'duration': "3:20",
                    'albumArt': "https://placehold.co/300x300/FF4500/ffffff?text=Blinding+Lights",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-40.mp3",
                    'uri': "spotify:track:energetic_10"
                }
            ],
            'calm': [
                {
                    'id': 'calm_1',
                    'title': "Weightless",
                    'artist': "Marconi Union",
                    'album': "Weightless",
                    'duration': "8:00",
                    'albumArt': "https://placehold.co/300x300/8a2be2/ffffff?text=Weightless",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3",
                    'uri': "spotify:track:calm_1"
                },
                {
                    'id': 'calm_2',
                    'title': "Clair de Lune",
                    'artist': "Claude Debussy",
                    'album': "Suite bergamasque",
                    'duration': "5:05",
                    'albumArt': "https://placehold.co/300x300/ff6b6b/ffffff?text=Clair+de+Lune",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
                    'uri': "spotify:track:calm_2"
                },
                {
                    'id': 'calm_3',
                    'title': "River Flows in You",
                    'artist': "Yiruma",
                    'album': "First Love",
                    'duration': "3:18",
                    'albumArt': "https://placehold.co/300x300/20b2aa/ffffff?text=River+Flows+in+You",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3",
                    'uri': "spotify:track:calm_3"
                },
                {
                    'id': 'calm_4',
                    'title': "Spiegel im Spiegel",
                    'artist': "Arvo Pärt",
                    'album': "Tabula Rasa",
                    'duration': "10:01",
                    'albumArt': "https://placehold.co/300x300/da70d6/ffffff?text=Spiegel+im+Spiegel",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-17.mp3",
                    'uri': "spotify:track:calm_4"
                },
                {
                    'id': 'calm_5',
                    'title': "Gymnopedie No.1",
                    'artist': "Erik Satie",
                    'album': "Gymnopedies",
                    'duration': "3:33",
                    'albumArt': "https://placehold.co/300x300/87CEEB/ffffff?text=Gymnopedie+No.1",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-41.mp3",
                    'uri': "spotify:track:calm_5"
                },
                {
                    'id': 'calm_6',
                    'title': "Clair de Lune",
                    'artist': "Claude Debussy",
                    'album': "Suite Bergamasque",
                    'duration': "5:05",
                    'albumArt': "https://placehold.co/300x300/87CEEB/ffffff?text=Clair+de+Lune",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-42.mp3",
                    'uri': "spotify:track:calm_6"
                },
                {
                    'id': 'calm_7',
                    'title': "Moonlight Sonata",
                    'artist': "Ludwig van Beethoven",
                    'album': "Piano Sonatas",
                    'duration': "5:20",
                    'albumArt': "https://placehold.co/300x300/87CEEB/ffffff?text=Moonlight+Sonata",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-43.mp3",
                    'uri': "spotify:track:calm_7"
                },
                {
                    'id': 'calm_8',
                    'title': "Meditation",
                    'artist': "Jules Massenet",
                    'album': "Thaïs",
                    'duration': "4:15",
                    'albumArt': "https://placehold.co/300x300/87CEEB/ffffff?text=Meditation",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-44.mp3",
                    'uri': "spotify:track:calm_8"
                }
            ],
            'romantic': [
                {
                    'id': 'romantic_1',
                    'title': "Perfect",
                    'artist': "Ed Sheeran",
                    'album': "÷ (Divide)",
                    'duration': "4:23",
                    'albumArt': "https://placehold.co/300x300/8a2be2/ffffff?text=Perfect",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-18.mp3",
                    'uri': "spotify:track:romantic_1"
                },
                {
                    'id': 'romantic_2',
                    'title': "All of Me",
                    'artist': "John Legend",
                    'album': "Love in the Future",
                    'duration': "4:29",
                    'albumArt': "https://placehold.co/300x300/ff6b6b/ffffff?text=All+of+Me",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-19.mp3",
                    'uri': "spotify:track:romantic_2"
                },
                {
                    'id': 'romantic_3',
                    'title': "Thinking Out Loud",
                    'artist': "Ed Sheeran",
                    'album': "x (Deluxe Edition)",
                    'duration': "4:41",
                    'albumArt': "https://placehold.co/300x300/20b2aa/ffffff?text=Thinking+Out+Loud",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-20.mp3",
                    'uri': "spotify:track:romantic_3"
                },
                {
                    'id': 'romantic_4',
                    'title': "At Last",
                    'artist': "Etta James",
                    'album': "At Last!",
                    'duration': "3:03",
                    'albumArt': "https://placehold.co/300x300/da70d6/ffffff?text=At+Last",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-21.mp3",
                    'uri': "spotify:track:romantic_4"
                },
                {
                    'id': 'romantic_5',
                    'title': "Make You Feel My Love",
                    'artist': "Adele",
                    'album': "19",
                    'duration': "3:32",
                    'albumArt': "https://placehold.co/300x300/FF69B4/ffffff?text=Make+You+Feel+My+Love",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-45.mp3",
                    'uri': "spotify:track:romantic_5"
                },
                {
                    'id': 'romantic_6',
                    'title': "All of Me",
                    'artist': "John Legend",
                    'album': "Love in the Future",
                    'duration': "4:29",
                    'albumArt': "https://placehold.co/300x300/FF69B4/ffffff?text=All+of+Me",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-46.mp3",
                    'uri': "spotify:track:romantic_6"
                },
                {
                    'id': 'romantic_7',
                    'title': "Thinking Out Loud",
                    'artist': "Ed Sheeran",
                    'album': "x",
                    'duration': "4:41",
                    'albumArt': "https://placehold.co/300x300/FF69B4/ffffff?text=Thinking+Out+Loud",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-47.mp3",
                    'uri': "spotify:track:romantic_7"
                },
                {
                    'id': 'romantic_8',
                    'title': "Love Story",
                    'artist': "Taylor Swift",
                    'album': "Fearless",
                    'duration': "3:55",
                    'albumArt': "https://placehold.co/300x300/FF69B4/ffffff?text=Love+Story",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-48.mp3",
                    'uri': "spotify:track:romantic_8"
                },
                {
                    'id': 'romantic_9',
                    'title': "Just the Way You Are",
                    'artist': "Bruno Mars",
                    'album': "Doo-Wops & Hooligans",
                    'duration': "3:40",
                    'albumArt': "https://placehold.co/300x300/FF69B4/ffffff?text=Just+the+Way+You+Are",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-49.mp3",
                    'uri': "spotify:track:romantic_9"
                },
                {
                    'id': 'romantic_10',
                    'title': "A Thousand Years",
                    'artist': "Christina Perri",
                    'album': "The Twilight Saga: Breaking Dawn - Part 1",
                    'duration': "4:45",
                    'albumArt': "https://placehold.co/300x300/FF69B4/ffffff?text=A+Thousand+Years",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-50.mp3",
                    'uri': "spotify:track:romantic_10"
                }
            ],
            'focused': [
                {
                    'id': 'focused_1',
                    'title': "Minecraft Theme",
                    'artist': "C418",
                    'album': "Minecraft - Volume Alpha",
                    'duration': "10:14",
                    'albumArt': "https://placehold.co/300x300/8a2be2/ffffff?text=Minecraft",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-22.mp3",
                    'uri': "spotify:track:focused_1"
                },
                {
                    'id': 'focused_2',
                    'title': "Gymnopedie No.1",
                    'artist': "Erik Satie",
                    'album': "Gymnopedies",
                    'duration': "3:33",
                    'albumArt': "https://placehold.co/300x300/ff6b6b/ffffff?text=Gymnopedie",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-23.mp3",
                    'uri': "spotify:track:focused_2"
                },
                {
                    'id': 'focused_3',
                    'title': "Experience",
                    'artist': "Ludovico Einaudi",
                    'album': "In a Time Lapse",
                    'duration': "5:24",
                    'albumArt': "https://placehold.co/300x300/20b2aa/ffffff?text=Experience",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-24.mp3",
                    'uri': "spotify:track:focused_3"
                },
                {
                    'id': 'focused_4',
                    'title': "Comptine d'un autre été",
                    'artist': "Yann Tiersen",
                    'album': "Amélie (Le Fabuleux Destin d'Amélie Poulain)",
                    'duration': "2:20",
                    'albumArt': "https://placehold.co/300x300/da70d6/ffffff?text=Comptine+d'un+autre+été",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-25.mp3",
                    'uri': "spotify:track:focused_4"
                },
                {
                    'id': 'focused_5',
                    'title': "Clair de Lune",
                    'artist': "Claude Debussy",
                    'album': "Suite Bergamasque",
                    'duration': "5:05",
                    'albumArt': "https://placehold.co/300x300/9370DB/ffffff?text=Clair+de+Lune",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-51.mp3",
                    'uri': "spotify:track:focused_5"
                },
                {
                    'id': 'focused_6',
                    'title': "Meditation from Thaïs",
                    'artist': "Jules Massenet",
                    'album': "Thaïs",
                    'duration': "4:15",
                    'albumArt': "https://placehold.co/300x300/9370DB/ffffff?text=Meditation+from+Thaïs",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-52.mp3",
                    'uri': "spotify:track:focused_6"
                },
                {
                    'id': 'focused_7',
                    'title': "Gymnopedie No. 1",
                    'artist': "Erik Satie",
                    'album': "Gymnopedies",
                    'duration': "3:33",
                    'albumArt': "https://placehold.co/300x300/9370DB/ffffff?text=Gymnopedie+No.+1",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-53.mp3",
                    'uri': "spotify:track:focused_7"
                },
                {
                    'id': 'focused_8',
                    'title': "Moonlight Sonata, 1st Movement",
                    'artist': "Ludwig van Beethoven",
                    'album': "Piano Sonatas",
                    'duration': "5:20",
                    'albumArt': "https://placehold.co/300x300/9370DB/ffffff?text=Moonlight+Sonata",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-54.mp3",
                    'uri': "spotify:track:focused_8"
                },
                {
                    'id': 'focused_9',
                    'title': "Pavane pour une infante défunte",
                    'artist': "Maurice Ravel",
                    'album': "Piano Works",
                    'duration': "6:15",
                    'albumArt': "https://placehold.co/300x300/9370DB/ffffff?text=Pavane+pour+une+infante+défunte",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-55.mp3",
                    'uri': "spotify:track:focused_9"
                },
                {
                    'id': 'focused_10',
                    'title': "The Seasons, Op. 37b: VI. June (Barcarolle)",
                    'artist': "Pyotr Ilyich Tchaikovsky",
                    'album': "The Seasons",
                    'duration': "4:50",
                    'albumArt': "https://placehold.co/300x300/9370DB/ffffff?text=The+Seasons",
                    'previewUrl': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-56.mp3",
                    'uri': "spotify:track:focused_10"
                }
            ]
        }
        
        # Get tracks for the mood and shuffle them for variety
        tracks = demo_tracks_data.get(mood, demo_tracks_data.get('happy', []))
        random.shuffle(tracks)
        
        # Return up to 12 tracks
        return tracks[:12]
    
    def get_track_uri(self, track_id):
        """
        Get Spotify URI for a track
        
        Args:
            track_id (str): The Spotify track ID
            
        Returns:
            str: The Spotify URI for the track
        """
        if self.demo_mode:
            return f"spotify:track:{track_id}"
        
        try:
            track = self.sp.track(track_id)
            # Check if track is None or doesn't contain expected structure
            if not track or 'uri' not in track:
                print("Warning: Spotify API returned unexpected track structure")
                return None
            return track['uri']
        except Exception as e:
            print(f"Error fetching track URI: {e}")
            return None
    
    def _format_duration(self, duration_ms):
        """Convert milliseconds to MM:SS format"""
        seconds = duration_ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"

# Example usage (for testing purposes)
if __name__ == "__main__":
    spotify_manager = SpotifyManager()
    
    # Test getting tracks for different moods
    moods = ['happy', 'sad', 'energetic']
    for mood in moods:
        print(f"\n--- {mood.capitalize()} Tracks ---")
        tracks = spotify_manager.get_mood_tracks(mood)
        for track in tracks[:3]:  # Show first 3 tracks
            print(f"{track['title']} by {track['artist']}")
