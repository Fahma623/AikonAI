import gradio as gr
import os
import logging
import random
import requests
import tempfile
from PIL import Image, ImageDraw
import io
import base64
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
GENRES = [
    "K-pop", "J-pop", "Synthwave", "Cyberpunk", "Future Bass",
    "Hyperpop", "Vaporwave", "Electronic", "Pop", "Hip-hop"
]

# Random idol ideas
IDOL_IDEAS = [
    "A digital diva from the year 3000",
    "A mysterious AI entity that sings in binary",
    "A virtual idol who exists only in the metaverse",
    "A cyberpunk street performer from Neo Tokyo",
    "A holographic pop star from a distant galaxy"
]

# Bio templates
BIO_TEMPLATES = [
    "{name} is a groundbreaking {genre} artist who has taken the music world by storm. {persona} With a unique blend of {genre} elements and futuristic sounds, {name} has created a signature style that resonates with audiences worldwide. Their performances are known for their high-energy and innovative use of technology, making them a pioneer in the digital music scene.",
    
    "Meet {name}, the {genre} sensation who has redefined what it means to be an artist in the digital age. {persona} Drawing inspiration from both classic {genre} and cutting-edge technology, {name} has developed a sound that is both nostalgic and forward-thinking. Their music has garnered a massive following of fans who are drawn to their authentic and boundary-pushing approach.",
    
    "The enigmatic {name} has emerged as one of the most exciting voices in {genre} music. {persona} With a background that defies conventional categorization, {name} brings a fresh perspective to the genre, incorporating elements of {genre} with experimental sound design. Their live performances are legendary, featuring stunning visuals and immersive audio experiences.",
    
    "{name} is not just a {genre} artist—they are a digital phenomenon. {persona} Breaking free from traditional musical constraints, {name} has created a new sonic landscape that challenges listeners' expectations. Their innovative approach to {genre} has earned them critical acclaim and a dedicated fanbase that spans the globe.",
    
    "In the ever-evolving world of {genre} music, {name} stands out as a true innovator. {persona} Their music seamlessly blends the familiar elements of {genre} with futuristic soundscapes, creating an auditory experience that is both comforting and exhilarating. {name}'s artistic vision extends beyond just music, encompassing visual art, fashion, and digital media."
]

# Lyrics templates
LYRICS_TEMPLATES = [
    """Title: Digital Dreams

[Verse 1]
In the neon lights of the city night
{name} takes flight, breaking through the digital divide
{genre} rhythms pulse through the air
A new sound that no one can compare

[Chorus]
We're living in a digital dream
Where reality and fantasy convene
{name} leads us to a higher plane
Where music flows like digital rain

[Verse 2]
{persona}
Breaking boundaries with every beat
Creating sounds that can't be beat
In this world of endless possibility
{name} brings us digital divinity""",

    """Title: Binary Heartbeat

[Verse 1]
{name} emerges from the digital void
With {genre} sounds that can't be destroyed
{persona}
Creating melodies that touch the soul
Making listeners lose control

[Chorus]
Binary heartbeat, digital soul
{name} makes us feel whole
In this world of ones and zeros
Music flows like digital heroes

[Verse 2]
The future of sound is here today
{name} shows us the digital way
{genre} elements blend with innovation
Creating a musical sensation""",

    """Title: Cyber Symphony

[Verse 1]
{name} conducts a cyber symphony
Where {genre} meets digital harmony
{persona}
Each note a pixel in the grand design
Creating music that's truly divine

[Chorus]
In this cyber symphony
{name} sets our spirits free
Digital dreams come alive
As we dance and thrive

[Verse 2]
The boundaries between real and virtual blur
As {name} creates sounds that stir
{genre} rhythms pulse through the night
As we dance in digital delight"""
]

# CSS for custom styling
custom_css = """
/* Main container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Background styling */
body {
    background-color: #0a0a0a;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(255, 0, 255, 0.05) 0%, transparent 20%),
        radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 20%),
        linear-gradient(to bottom, #0a0a0a, #1a1a1a);
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Neon text effect */
.neon-text {
    color: #fff;
    text-shadow: 
        0 0 5px #fff,
        0 0 10px #fff,
        0 0 20px #ff00ff,
        0 0 30px #ff00ff,
        0 0 40px #ff00ff;
    font-weight: bold;
    letter-spacing: 2px;
}

/* Card styling */
.card {
    background-color: rgba(20, 20, 30, 0.8);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
    border: 1px solid rgba(255, 0, 255, 0.2);
    backdrop-filter: blur(10px);
}

/* Button styling */
button {
    background: linear-gradient(45deg, #9b4dca, #4d9bca);
    border: none;
    border-radius: 30px;
    color: white;
    padding: 12px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.4);
    position: relative;
    overflow: hidden;
    z-index: 1;
}

button:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #9b4dca, #4d9bca, #9b4dca);
    background-size: 200% 200%;
    z-index: -1;
    transition: all 0.5s ease;
    animation: gradient-shift 3s ease infinite;
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

button:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 15px rgba(155, 77, 202, 0.5);
    color: white;
}

button:active {
    transform: translateY(1px);
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.4);
}

/* Primary button styling */
.btn-primary {
    font-size: 1.2em;
    padding: 15px 40px;
    background: linear-gradient(45deg, #9b4dca, #4d9bca);
    border: none;
    border-radius: 30px;
    color: white;
    font-weight: bold;
    box-shadow: 0 0 12px rgba(155, 77, 202, 0.4);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.btn-primary:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #9b4dca, #4d9bca, #9b4dca);
    background-size: 200% 200%;
    z-index: -1;
    transition: all 0.5s ease;
    animation: gradient-shift 3s ease infinite;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 15px rgba(155, 77, 202, 0.5);
    color: white;
}

.btn-primary:active {
    transform: translateY(1px);
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.4);
}

/* Secondary button styling */
.btn-secondary {
    font-size: 1.1em;
    padding: 12px 30px;
    background: rgba(30, 30, 40, 0.8);
    border: 1px solid rgba(155, 77, 202, 0.3);
    border-radius: 30px;
    color: white;
    font-weight: bold;
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.btn-secondary:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, rgba(155, 77, 202, 0.2), rgba(77, 155, 202, 0.2));
    background-size: 200% 200%;
    z-index: -1;
    transition: all 0.5s ease;
    animation: gradient-shift 3s ease infinite;
}

.btn-secondary:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 12px rgba(155, 77, 202, 0.4);
    background: rgba(40, 40, 50, 0.8);
    border-color: rgba(155, 77, 202, 0.5);
    color: white;
}

.btn-secondary:active {
    transform: translateY(1px);
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.3);
}

/* Input styling */
input, select, textarea {
    background-color: rgba(30, 30, 40, 0.8);
    border: 1px solid rgba(255, 0, 255, 0.3);
    border-radius: 10px;
    color: white;
    padding: 12px;
    transition: all 0.3s ease;
}

input:focus, select:focus, textarea:focus {
    border-color: #ff00ff;
    box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
    outline: none;
}

/* Tab styling */
.tabs {
    background-color: rgba(20, 20, 30, 0.8);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
    border: 1px solid rgba(255, 0, 255, 0.2);
}

.tab-nav {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.tab-button {
    background: rgba(30, 30, 40, 0.8);
    border: 1px solid rgba(255, 0, 255, 0.3);
    border-radius: 30px;
    color: white;
    padding: 10px 20px;
    margin: 0 5px;
    font-weight: bold;
    transition: all 0.3s ease;
    cursor: pointer;
}

.tab-button.active {
    background: linear-gradient(45deg, #ff00ff, #00ffff);
    box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .card {
        padding: 15px;
    }
    
    button {
        width: 100%;
        margin-bottom: 10px;
    }
}

/* Output styling */
.output-card {
    background-color: rgba(20, 20, 30, 0.9);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    border: 1px solid rgba(0, 255, 255, 0.2);
}

.output-title {
    color: #00ffff;
    font-size: 1.2em;
    margin-bottom: 10px;
    text-shadow: 0 0 5px #00ffff;
}

/* Image styling */
.album-cover {
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
    transition: transform 0.3s ease;
}

.album-cover:hover {
    transform: scale(1.02);
}

/* Start button styling */
#start-btn {
    font-size: 1.2em;
    padding: 15px 40px;
    background: linear-gradient(45deg, #9b4dca, #4d9bca);
    border: none;
    border-radius: 30px;
    color: white;
    font-weight: bold;
    box-shadow: 0 0 12px rgba(155, 77, 202, 0.4);
    transition: all 0.3s ease;
    cursor: pointer;
    margin-top: 20px;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

#start-btn:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #9b4dca, #4d9bca, #9b4dca);
    background-size: 200% 200%;
    z-index: -1;
    transition: all 0.5s ease;
    animation: gradient-shift 3s ease infinite;
}

#start-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 15px rgba(155, 77, 202, 0.5);
    color: white;
}

#start-btn:active {
    transform: translateY(1px);
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.4);
}

/* Form styling */
.form-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: rgba(20, 20, 30, 0.8);
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
    border: 1px solid rgba(255, 0, 255, 0.2);
}

/* Output container */
.output-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: rgba(20, 20, 30, 0.8);
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    border: 1px solid rgba(0, 255, 255, 0.2);
}

/* Button container */
.button-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

/* Color scheme */
:root {
    --primary-color: #ff00ff;
    --secondary-color: #00ffff;
    --accent-color: #ff6600;
    --background-color: #0a0a0a;
    --card-color: rgba(20, 20, 30, 0.8);
    --text-color: #ffffff;
    --border-color: rgba(255, 0, 255, 0.2);
}

/* Gradio specific overrides */
.gradio-container {
    background-color: var(--background-color) !important;
}

.tabs {
    background-color: var(--card-color) !important;
}

.tab-nav {
    background-color: var(--card-color) !important;
}

.tab-nav button {
    background-color: rgba(30, 30, 40, 0.8) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--border-color) !important;
}

.tab-nav button.selected {
    background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)) !important;
    box-shadow: 0 0 10px rgba(255, 0, 255, 0.5) !important;
}

/* Fix for button alignment */
.flex {
    display: flex;
    justify-content: center;
    gap: 10px;
}

/* Gradio specific overrides for buttons */
.gradio-container button {
    background: linear-gradient(45deg, #9b4dca, #4d9bca) !important;
    border: none !important;
    border-radius: 30px !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.4) !important;
    transition: all 0.3s ease !important;
}

.gradio-container button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 0 15px rgba(155, 77, 202, 0.5) !important;
}

.gradio-container button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 0 8px rgba(155, 77, 202, 0.4) !important;
}
"""

def generate_bio(name, genre, persona):
    """Generate an idol bio using templates."""
    try:
        logger.info(f"Generating bio for {name}")
        
        # Select a random template and fill it with the provided information
        template = random.choice(BIO_TEMPLATES)
        bio = template.format(name=name, genre=genre, persona=persona)
        
        return bio
    except Exception as e:
        logger.error(f"Error generating bio: {str(e)}")
        return f"Error generating bio: {str(e)}"

def generate_lyrics(name, genre, persona):
    """Generate song lyrics using templates."""
    try:
        logger.info(f"Generating lyrics for {name}")
        
        # Select a random template and fill it with the provided information
        template = random.choice(LYRICS_TEMPLATES)
        lyrics = template.format(name=name, genre=genre, persona=persona)
        
        return lyrics
    except Exception as e:
        logger.error(f"Error generating lyrics: {str(e)}")
        return f"Error generating lyrics: {str(e)}"

def generate_image(name, genre, persona):
    """Generate an album cover using Stable Diffusion."""
    try:
        logger.info(f"Generating album cover for {name}")
        prompt = f"Create a stunning album cover for {name}, a {genre} artist. Style: {persona}. Make it cyberpunk, futuristic, with vibrant colors and holographic elements. Square format, suitable for an album cover."
        
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
        
        # Get API key from environment variable
        api_key = os.environ.get("HUGGINGFACE_API_KEY")
        if not api_key:
            logger.warning("HUGGINGFACE_API_KEY not found in environment variables. Using placeholder image.")
            return create_placeholder_image(name, genre)
            
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Try to generate the image with retries
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt+1}/{max_retries} to generate image")
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
                
                if response.status_code == 200:
                    # Success! Create a temporary file with a unique name
                    temp_dir = tempfile.gettempdir()
                    image_path = os.path.join(temp_dir, f"album_cover_{random.randint(1000, 9999)}.png")
                    
                    # Save the image
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                        
                    # Verify the image can be opened
                    try:
                        Image.open(image_path)
                        logger.info(f"Successfully generated image for {name}")
                        return image_path
                    except Exception as e:
                        logger.error(f"Error verifying image: {str(e)}")
                        # Continue to next retry or fallback
                
                elif response.status_code == 503:
                    logger.warning(f"API is loading model (503 error). Attempt {attempt+1}/{max_retries}")
                    # Wait before retrying
                    time.sleep(retry_delay)
                    continue
                
                else:
                    logger.error(f"API request failed with status code {response.status_code}")
                    # If we've tried all retries, create a placeholder
                    if attempt == max_retries - 1:
                        return create_placeholder_image(name, genre)
                    # Otherwise, wait and retry
                    time.sleep(retry_delay)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error on attempt {attempt+1}: {str(e)}")
                # If we've tried all retries, create a placeholder
                if attempt == max_retries - 1:
                    return create_placeholder_image(name, genre)
                # Otherwise, wait and retry
                time.sleep(retry_delay)
        
        # If we get here, all retries failed
        logger.error("All image generation attempts failed")
        return create_placeholder_image(name, genre)
            
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return create_placeholder_image(name, genre)

def create_placeholder_image(name, genre):
    """Create a placeholder image when the API fails."""
    try:
        logger.info(f"Creating placeholder image for {name}")
        
        # Create a more visually appealing placeholder image
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color=(20, 20, 30))
        draw = ImageDraw.Draw(image)
        
        # Add a gradient background
        for y in range(height):
            r = int(20 + (y / height) * 40)
            g = int(20 + (y / height) * 30)
            b = int(30 + (y / height) * 50)
            for x in range(width):
                # Add some noise/variation
                noise = random.randint(-10, 10)
                draw.point((x, y), fill=(r + noise, g + noise, b + noise))
        
        # Add some colorful elements
        colors = [
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (255, 0, 0)     # Red
        ]
        
        # Add some geometric shapes
        for _ in range(5):
            shape_type = random.choice(['circle', 'rectangle', 'line'])
            color = random.choice(colors)
            
            if shape_type == 'circle':
                x = random.randint(0, width)
                y = random.randint(0, height)
                radius = random.randint(20, 100)
                draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline=color, width=3)
            
            elif shape_type == 'rectangle':
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = random.randint(0, width)
                y2 = random.randint(0, height)
                draw.rectangle((x1, y1, x2, y2), outline=color, width=3)
            
            else:  # line
                x1, y1 = random.randint(0, width), random.randint(0, height)
                x2, y2 = random.randint(0, width), random.randint(0, height)
                draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
        
        # Add some glowing effects
        for _ in range(10):
            x = random.randint(0, width)
            y = random.randint(0, height)
            color = random.choice(colors)
            for r in range(5, 0, -1):
                alpha = int(255 * (1 - r/5))
                draw.ellipse((x-r, y-r, x+r, y+r), fill=(color[0], color[1], color[2], alpha))
        
        # Add text
        try:
            from PIL import ImageFont
            # Try to use a system font
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
                
            # Add the idol name with a glow effect
            text = name
            text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (200, 40)
            x = (width - text_width) // 2
            y = (height - text_height) // 2 - 50
            
            # Draw text shadow/glow
            for offset in range(10, 0, -1):
                alpha = int(255 * (1 - offset/10))
                draw.text((x+offset, y+offset), text, font=font, fill=(255, 255, 255, alpha))
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=(255, 255, 255))
            
            # Add the genre with a different style
            text = genre
            text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (200, 40)
            x = (width - text_width) // 2
            y = (height - text_height) // 2 + 50
            
            # Draw text shadow/glow
            for offset in range(10, 0, -1):
                alpha = int(255 * (1 - offset/10))
                draw.text((x+offset, y+offset), text, font=font, fill=(255, 0, 255, alpha))
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=(255, 0, 255))
            
        except Exception as e:
            logger.error(f"Error adding text to placeholder: {str(e)}")
        
        # Save the image
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, f"placeholder_{random.randint(1000, 9999)}.png")
        image.save(image_path)
        
        return image_path
    except Exception as e:
        logger.error(f"Error creating placeholder image: {str(e)}")
        return None

def randomize_idea():
    """Generate random idol idea."""
    try:
        name = f"AI-{random.randint(1000, 9999)}"
        genre = random.choice(GENRES)
        persona = random.choice(IDOL_IDEAS)
        return name, genre, persona
    except Exception as e:
        logger.error(f"Error in randomize: {str(e)}")
        return "Error", "Error", "Error"

def generate_idol(name, genre, persona):
    """Generate all idol content."""
    try:
        if not name or not genre or not persona:
            return "Please fill in all fields", "All fields are required", None
            
        logger.info(f"Generating idol content for {name}")
        
        # Generate content with error handling
        bio = generate_bio(name, genre, persona)
        lyrics = generate_lyrics(name, genre, persona)
        image_path = generate_image(name, genre, persona)
        
        # Check if image generation failed
        if image_path is None:
            return bio, lyrics, None
            
        return bio, lyrics, image_path
    except Exception as e:
        logger.error(f"Error generating idol: {str(e)}")
        return f"Error: {str(e)}", "Error generating content", None

# Create the interface with custom theme
with gr.Blocks(css=custom_css, theme=gr.themes.Base(primary_hue="purple", secondary_hue="cyan")) as app:
    # Create a state variable to track the current page
    current_page = gr.State(0)
    
    # Create the welcome page
    with gr.Column(visible=True) as welcome_page:
        gr.Markdown(
            """
            <div style="text-align: center; padding: 50px 0;">
                <h1 class="neon-text" style="font-size: 3em; margin-bottom: 20px;">🎤 AikonAI</h1>
                <h2 class="neon-text" style="font-size: 1.8em; margin-bottom: 40px;">AI Idol Generator ✨</h2>
                <p style="font-size: 1.2em; margin-bottom: 30px;">Create your own virtual idol with AI-generated bios, lyrics, and album covers</p>
            </div>
            """,
            elem_classes="card"
        )
        start_btn = gr.Button("Start Creating", elem_classes="btn-primary", size="lg")
    
    # Create the input page
    with gr.Column(visible=False) as input_page:
        gr.Markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 class="neon-text">Create Your AI Idol</h2>
                <p>Fill in the details below to generate your unique virtual idol</p>
            </div>
            """,
            elem_classes="card"
        )
        
        with gr.Column(elem_classes="form-container"):
            name = gr.Textbox(
                label="🎤 Idol Name",
                placeholder="Enter a name for your AI idol...",
                elem_classes="input-field"
            )
            genre = gr.Dropdown(
                choices=GENRES,
                label="🎵 Genre",
                elem_classes="input-field"
            )
            persona = gr.Textbox(
                label="💫 Idol Persona / Vibe",
                placeholder="Describe your idol's personality and style...",
                elem_classes="input-field"
            )
            
            with gr.Row(elem_classes="button-container"):
                randomize_btn = gr.Button("🎲 Randomize", elem_classes="btn-secondary")
                generate_btn = gr.Button("🎤 Generate Idol", elem_classes="btn-primary")
    
    # Create the output page
    with gr.Column(visible=False) as output_page:
        gr.Markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 class="neon-text">Your AI Idol</h2>
                <p>Here's your generated virtual idol content</p>
            </div>
            """,
            elem_classes="card"
        )
        
        with gr.Column(elem_classes="output-container"):
            bio_output = gr.Textbox(
                label="🧬 Idol Bio",
                lines=5,
                elem_classes="output-field"
            )
            lyrics_output = gr.Textbox(
                label="🎶 Song Lyrics",
                lines=8,
                elem_classes="output-field"
            )
            image_output = gr.Image(
                label="🎨 Album Cover",
                type="filepath",
                elem_classes="album-cover"
            )
            
            with gr.Row(elem_classes="button-container"):
                back_btn = gr.Button("← Back to Input", elem_classes="btn-secondary")
                new_idol_btn = gr.Button("Create New Idol", elem_classes="btn-primary")
    
    # Define page navigation functions
    def show_welcome():
        return {
            welcome_page: gr.update(visible=True),
            input_page: gr.update(visible=False),
            output_page: gr.update(visible=False)
        }
    
    def show_input():
        return {
            welcome_page: gr.update(visible=False),
            input_page: gr.update(visible=True),
            output_page: gr.update(visible=False)
        }
    
    def show_output():
        return {
            welcome_page: gr.update(visible=False),
            input_page: gr.update(visible=False),
            output_page: gr.update(visible=True)
        }
    
    # Event handlers
    start_btn.click(
        fn=show_input,
        inputs=None,
        outputs=[welcome_page, input_page, output_page]
    )
    
    randomize_btn.click(
        fn=randomize_idea,
        inputs=None,
        outputs=[name, genre, persona]
    )
    
    generate_btn.click(
        fn=generate_idol,
        inputs=[name, genre, persona],
        outputs=[bio_output, lyrics_output, image_output]
    ).then(
        fn=show_output,
        inputs=None,
        outputs=[welcome_page, input_page, output_page]
    )
    
    back_btn.click(
        fn=show_input,
        inputs=None,
        outputs=[welcome_page, input_page, output_page]
    )
    
    new_idol_btn.click(
        fn=show_welcome,
        inputs=None,
        outputs=[welcome_page, input_page, output_page]
    )

if __name__ == "__main__":
    logger.info("Starting AikonAI application...")
    app.launch() 