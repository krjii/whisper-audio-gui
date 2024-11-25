# Whisper Audio GUI

## Overview

This Python application provides a graphical user interface (GUI) to transcribe audio files using **OpenAI's Whisper AI**. Built with **PySide6**, the project offers an intuitive way to process audio files for transcription, leveraging the capabilities of Whisper AI. Dependency management is handled by **Poetry**, ensuring an organized and reproducible environment.

---

## Features

- **File Selection:** Browse and load audio files for transcription.
- **Whisper AI Integration:** Automatically transcribe audio files using the Whisper AI model.
- **User-Friendly GUI:** Built with PySide6 for a seamless user experience.
- **Support for Various Formats:** Accepts common audio file types like MP3, WAV, and others.

---

## Prerequisites

- Python 3.9 or later
- Poetry for dependency management
- FFmpeg (required by Whisper for media processing)

---

## Installation

Follow these steps to install and set up the project:

```bash
# Step 1: Clone the Repository
git clone https://github.com/krjii/whisper-audio-gui.git
cd whisper-audio-gui

# Step 2: Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Step 3: Install Dependencies
poetry install

# Step 4: Install FFmpeg
# For Ubuntu/Debian:
sudo apt update
sudo apt install ffmpeg

# For macOS (using Homebrew):
brew install ffmpeg

# For Windows:
# Download and install FFmpeg from https://ffmpeg.org/download.html

# Step 5: Activate the Poetry Environment
poetry shell

# Step 6: Run the Application
python main.py

## Usage

1. **Run the Application**:
   Launch the application by running the following command in the terminal:

   ```bash
   python app.py
   

### Key Files and Directories

- **`src/main.py`**:
  - The main script to initialize and launch the application.
- **`src/presentation/`**:
  - Contains all GUI-related files, including the `.ui` design file and its Python implementation.
- **`tests/`**:
  - Contains unit tests to validate application functionality and reliability.
- **`pyproject.toml`**:
  - Poetry configuration file for managing dependencies and project metadata.
- **`README.md`**:
  - This documentation file, providing setup instructions, usage, and other details.
- **`LICENSE`**:
  - The license under which the project is distributed.

This structure ensures the project is well-organized, modular, and easy to navigate for development, testing, and maintenance.


## Dependencies

The following dependencies are required for this project and are managed using **Poetry**:

- **`pyside6`**: For building the graphical user interface.
- **`openai-whisper`**: Whisper AI library for audio transcription.
- **`ffmpeg-python`**: Python wrapper for FFmpeg to handle audio file processing.
- **`pytest`** (development dependency): For running unit tests.

### Managing Dependencies with Poetry

To add new dependencies, use the following command:

```bash
poetry add <package_name>
