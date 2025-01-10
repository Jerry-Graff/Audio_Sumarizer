# Audio Summarizer API

A FastAPI application that accepts an audio file upload, transcribes it using OpenAI's Whisper API, and summarizes the transcript using ChatGPT. This project serves as a guide to working with FastAPI endpoints and integrating OpenAI's APIs for transcription and summarization tasks.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Development](#development)
- [License](#license)

## Features

- **Audio Transcription:** Utilizes OpenAI's Whisper API to transcribe uploaded audio files.
- **Text Summarization:** Uses ChatGPT (GPT-3.5 Turbo) to generate summaries of transcribed text.
- **File Handling:** Efficiently handles file uploads, temporary storage, and cleanup.
- **Modular Design:** Clean separation of concerns with helper functions for transcription and summarization.

## Prerequisites

- **Python 3.7+**
- An OpenAI API key. You can sign up at [OpenAI](https://openai.com/) and generate an API key.
- Basic knowledge of Python, FastAPI, and RESTful APIs.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/audio-summarizer.git
   cd audio-summarizer