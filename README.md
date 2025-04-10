---
title: AikonAI
emoji: 🎭
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: "4.19.2"
app_file: app.py
pinned: false
---

# 🎤 AikonAI – AI Idol Generator ✨

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-3.50.2%2B-green)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AikonAI is an innovative application that generates virtual idols with AI-powered bios, lyrics, and album covers. Create your own digital pop star with just a few clicks!

![AikonAI Screenshot](screenshot.png)

## ✨ Features

- **🎤 Idol Bio Generation**: Create unique, detailed bios for your virtual idols
- **🎵 Song Lyrics Generation**: Generate themed lyrics based on your idol's persona
- **🎨 Album Cover Generation**: Create eye-catching album covers with AI
- **🎲 Randomization**: Get instant inspiration with the randomize feature
- **💫 Modern UI**: Enjoy a sleek, responsive interface with smooth transitions

## 🚀 Live Demo

Coming soon on Hugging Face Spaces!

## 🛠️ Local Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Fahma623/AikonAI.git
   cd AikonAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Hugging Face API key:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   ```
   Get your API key from [Hugging Face](https://huggingface.co/settings/tokens)

4. Run the application:
   ```bash
   python app.py
   ```

## 🌐 Hugging Face Spaces Deployment

To deploy this application on Hugging Face Spaces:

1. Create a new Space on Hugging Face (https://huggingface.co/spaces)
2. Choose "Gradio" as the SDK
3. Connect to your GitHub repository or upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. Set the following environment variables in your Space settings:
   - `HUGGINGFACE_API_KEY`: Your Hugging Face API key
5. Your Space will automatically build and deploy the application

## 🧠 How It Works

AikonAI uses a combination of template-based generation and AI-powered image creation:

- **Text Generation**: Uses predefined templates with dynamic content insertion
- **Image Generation**: Leverages Hugging Face's Stable Diffusion model
- **UI**: Built with Gradio for a responsive, modern interface

## 🛠️ Technologies Used

- **Gradio**: For the web interface
- **Hugging Face Inference API**: For image generation
- **Python**: For backend logic
- **Custom CSS**: For styling

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Created with ❤️ by Fahma Fathima