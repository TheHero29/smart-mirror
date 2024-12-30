import cv2
from fer import FER
import pyttsx3
import threading
import queue
import time
import signal
import sys
# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 135)  # Speed of speech (words per minute)
engine.setProperty('volume', 1)  # Volume level 0-1

# Initialize face detector 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize FER (Facial Emotion Recognition) model
emotion_detector = FER()

# Start the webcam
cap = cv2.VideoCapture(0)

# Queue for handling compliments
compliment_queue = queue.Queue()

# Variable to store the last detected emotion and its time
last_emotion = None
last_detection_time = time.time()

# Emotion to compliment dictionary
emotion_compliments = {
    'happy': "Your smile is radiant!",
    'neutral': "You have a calm presence.",
    'sad': "Don't worry, this too shall pass.",
    'surprise': "Wow, you look surprised!",
    'fear': "Don't be scared, everything will be okay.",
    'angry': "It's okay to be upset, take a deep breath.",
}

# Function to speak the compliment (runs in a separate thread)
def speak_compliment():
    while True:
        compliment = compliment_queue.get()  
        if compliment == "exit":
            break  
        engine.say(compliment)
        engine.runAndWait()

# Start the speaking thread
speak_thread = threading.Thread(target=speak_compliment)
speak_thread.daemon = True  # Make it a daemon thread to exit when the program ends
speak_thread.start()

# Variable to store the last compliment
compliment = ""

def shutdown(signum, frame):
    print("Shutting down...")
    compliment_queue.put("exit")  
    cap.release()  
    cv2.destroyAllWindows()  
    sys.exit(0)  

# Set up signal handling for shutdown on SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, shutdown)

# for real-time recognition and display
while True:
    ret, frame = cap.read()
    
    # Convert the frame to grayscale (required for face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7, minSize=(30, 30))

    # Iterate over all detected faces
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the face region for emotion detection
        face = frame[y:y + h, x:x + w]

        # Use FER to analyze the emotion of the face
        emotion, score = emotion_detector.top_emotion(face)

        # Only update and speak the compliment if emotion has changed in last 4 secs
        if emotion != last_emotion and (time.time() - last_detection_time > 4):
            compliment = emotion_compliments.get(emotion, "You're unique in your own way!")
            compliment_queue.put(compliment)  
            last_emotion = emotion 
            last_detection_time = time.time()

        # Display the compliment text on the image
        cv2.putText(frame, f"{compliment}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Show the resulting image with face and compliment text
    cv2.imshow('Face and Emotion Detection', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

shutdown(0, 0)