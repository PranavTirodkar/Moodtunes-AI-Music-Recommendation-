// DOM Elements
const getStartedBtn = document.getElementById('getStartedBtn');
const moodCards = document.querySelectorAll('.mood-card');
const customMoodInput = document.getElementById('customMoodInput');
const analyzeCustomMoodBtn = document.getElementById('analyzeCustomMood');
const moodSelector = document.getElementById('moodSelector');
const recommendationsSection = document.getElementById('recommendations');
const recommendationsGrid = document.getElementById('recommendationsGrid');
const loadingIndicator = document.getElementById('loadingIndicator');
const navLinks = document.querySelectorAll('.nav-link');
const contactForm = document.getElementById('contactForm');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log("MoodTunes App Loaded");
    
    // Set up navigation
    setupNavigation();
    
    // Set up contact form
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
});

getStartedBtn.addEventListener('click', () => {
    // Show the mood selector when user clicks "Get Started"
    moodSelector.style.display = 'block';
    
    // Scroll to the mood selector
    moodSelector.scrollIntoView({ behavior: 'smooth' });
});

moodCards.forEach(card => {
    card.addEventListener('click', () => {
        const mood = card.dataset.mood;
        showRecommendations(mood);
    });
});

analyzeCustomMoodBtn.addEventListener('click', () => {
    const customMoodText = customMoodInput.value.trim();
    if (customMoodText) {
        // In a real app, this would send the text to your AI model
        // For now, we'll simulate by detecting keywords
        const detectedMood = detectMoodFromText(customMoodText);
        showRecommendations(detectedMood);
    } else {
        alert("Please describe your mood first!");
    }
});

// Functions
function setupNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active class
            navLinks.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all sections except hero content
            const moodSelector = document.getElementById('moodSelector');
            const recommendations = document.getElementById('recommendations');
            
            if (moodSelector) moodSelector.style.display = 'none';
            if (recommendations) recommendations.style.display = 'none';
            
            // Show the corresponding section
            const sectionId = this.getAttribute('data-section');
            if (sectionId) {
                const section = document.getElementById(sectionId);
                if (section) {
                    section.style.display = 'block';
                    section.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

function handleContactForm(e) {
    e.preventDefault();
    
    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // In a real app, you would send this to a server
    // For now, we'll just show a success message
    alert(`Thank you for your message, ${name}! We'll get back to you soon.`);
    
    // Reset form
    contactForm.reset();
}

function detectMoodFromText(text) {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('happy') || lowerText.includes('joy') || lowerText.includes('excited')) {
        return 'happy';
    } else if (lowerText.includes('sad') || lowerText.includes('depressed') || lowerText.includes('cry')) {
        return 'sad';
    } else if (lowerText.includes('energy') || lowerText.includes('workout') || lowerText.includes('party')) {
        return 'energetic';
    } else if (lowerText.includes('relax') || lowerText.includes('peace') || lowerText.includes('calm')) {
        return 'calm';
    } else if (lowerText.includes('love') || lowerText.includes('romantic') || lowerText.includes('heart')) {
        return 'romantic';
    } else if (lowerText.includes('focus') || lowerText.includes('study') || lowerText.includes('concentrate')) {
        return 'focused';
    } else {
        return 'happy';
    }
}

async function showRecommendations(mood) {
    loadingIndicator.style.display = 'block';
    recommendationsGrid.innerHTML = '';
    
    try {
        const response = await fetch(`/api/recommendations/${mood}`);
        const data = await response.json();
        loadingIndicator.style.display = 'none';
        
        const tracks = data.tracks || [];
        tracks.forEach(track => {
            const trackCard = createTrackCard(track);
            recommendationsGrid.appendChild(trackCard);
        });
        
        // Show recommendations section
        recommendationsSection.style.display = 'block';
        
        // Scroll to recommendations
        recommendationsSection.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error("Error fetching recommendations:", error);
        loadingIndicator.style.display = 'none';
        recommendationsGrid.innerHTML = '<p>Error loading recommendations. Please try again.</p>';
    }
}

function createTrackCard(track) {
    const card = document.createElement('div');
    card.className = 'track-card';
    card.innerHTML = `
        <div class="album-art" style="background-image: url('${track.albumArt}')"></div>
        <div class="track-info">
            <h3>${track.title}</h3>
            <p>${track.artist}</p>
            <p>${track.album} • ${track.duration}</p>
            <button class="play-button" data-track-title="${track.title}" data-track-artist="${track.artist}">
                <i class="fas fa-play"></i>
            </button>
            <div class="audio-player">
                <audio controls>
                    <source src="${track.previewUrl || '#'}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
        </div>
    `;
    
    const playButton = card.querySelector('.play-button');
    const audioPlayer = card.querySelector('.audio-player');
    const audioElement = card.querySelector('audio');
    
    playButton.addEventListener('click', () => {
        // Toggle play/pause
        if (playButton.classList.contains('playing')) {
            // Pause the audio
            audioElement.pause();
            playButton.innerHTML = '<i class="fas fa-play"></i>';
            playButton.classList.remove('playing');
        } else {
            // Play the audio
            audioElement.play().then(() => {
                playButton.innerHTML = '<i class="fas fa-pause"></i>';
                playButton.classList.add('playing');
                audioPlayer.style.display = 'block';
            }).catch(error => {
                console.error('Error playing audio:', error);
                alert('Unable to play audio. This might be a demo track with no preview available.');
            });
        }
    });
    
    // When audio ends, reset the play button
    audioElement.addEventListener('ended', () => {
        playButton.innerHTML = '<i class="fas fa-play"></i>';
        playButton.classList.remove('playing');
    });
    
    return card;
}