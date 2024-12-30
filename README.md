
# Compliment System for smart mirror

This project is a compliment system for smart mirror that detects emotions using facial recognition and provides a compliment based on the detected emotion. The program utilizes OpenCV for face detection, FER (Facial Emotion Recognition) library for emotion analysis, and pyttsx3 for text-to-speech functionality.

## Features

- **Real-Time Face Detection**: Uses OpenCV's Haar Cascade Classifier for detecting faces in real-time.
- **Emotion Recognition**: Analyzes the detected face using the FER library to identify emotions such as happy, sad, neutral, etc.
- **Compliments Based on Emotion**: When an emotion is detected, a corresponding compliment is spoken and displayed on the mirror.
- **Text-to-Speech**: Compliments are spoken out loud using the pyttsx3 text-to-speech engine.
- **Graceful Shutdown**: The program ensures that all resources are properly released when the user quits.

## Challenges faced -
### 1.Too frequent emotion change:
Problem: emotions were changing too frequently and queue was getting filled unnecessarily
Solution: compliment will be pushed to queue only if there is a emotion change in last 5 secs

### 2.Audio and Speech Issues:
Problem: The camera video would pause during text-to-speech
Solution: Used a separate thread and a queue to handle speech so it doesn’t block the main program.

## Setup and Usage

### 1. Clone the repository:

Clone the repository to your local machine:

```bash
git clone https://github.com/TheHero29/smart-mirror.git
cd smart-mirror
```

### 2. Create a virtual environment (to avoid version conflicts)

For Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:
```bash
python3 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

To install the required dependencies, you can use the following `pip` command:

```bash
pip install -r requirements.txt
```

### 4. Run the program
```bash
python3 main.py
```

### 5. Exit the Program

To stop the program, you can press `Ctrl+C` in the terminal.

## Troubleshooting

### 1. Qt Platform Plugin Issue

If you encounter the error message `Could not find the Qt platform plugin "wayland"`, you can try setting the `QT_QPA_PLATFORM` environment variable to `offscreen` to bypass this issue:

For **Linux/MacOS**:

```bash
export QT_QPA_PLATFORM=offscreen
```

This will allow the program to run without the GUI, though it might limit some visual aspects.

### 2. Camera Access Issues

If the webcam feed isn't appearing, consider the following steps:
- Ensure the webcam is properly connected to your system.
- Check for other applications that may be using the camera and close them.
- On Linux systems, ensure that your user has permissions to access the camera.

### 3. Speech Issues

If the text-to-speech engine is not working, ensure that `pyttsx3` is properly installed. You can also test it with a simple script to verify that your system's sound configuration is correct.

### 4. Emotion Detection Issues

- Make sure you're properly facing the camera with enough lighting.
- FER (Facial Emotion Recognition) may have limitations in different lighting conditions or face orientations.
- The program may not work well with certain face shapes or emotions under specific conditions.
