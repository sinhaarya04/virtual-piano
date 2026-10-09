# Virtual Piano

A Python desktop application that lets you play a virtual piano using your webcam and hand tracking. The application uses OpenCV and MediaPipe to track your index finger and play piano notes when you touch different zones on the screen.

## Features

- Real-time hand tracking using MediaPipe
- Virtual piano keyboard with 7 keys (C, D, E, F, G, A, B)
- Visual feedback when keys are pressed
- Generated piano sounds using sine waves
- Simple and intuitive interface

## Requirements

- Python 3.7 or higher
- Webcam
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository or download the files
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python virtual_piano.py
   ```
2. Position your hand in front of the webcam
3. Use your index finger to touch the virtual piano keys at the bottom of the screen
4. Press 'q' to quit the application

## How it Works

The application uses MediaPipe Hands to track your hand landmarks in real-time. It specifically tracks the index fingertip (landmark 8) and maps its position to the virtual piano keys. When your fingertip touches a key area, the corresponding note is played using generated sine wave sounds.

## Notes

- Make sure your webcam is properly connected and accessible
- Ensure good lighting for better hand tracking
- The application works best when your hand is clearly visible in the frame
- The virtual piano keys are displayed at the bottom of the screen 