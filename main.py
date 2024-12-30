import cv2
from fer import FER

# Initialize face detector 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize FER (Facial Emotion Recognition) model
emotion_detector = FER()

# Start the webcam
cap = cv2.VideoCapture(0)

# for real-time recognition
while True:
    ret, frame = cap.read()

    # Convert the frame to grayscale (required for face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Iterate over all detected faces
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the face region
        face = frame[y:y + h, x:x + w]

        # Use FER to analyze the emotion of the face
        emotion, score = emotion_detector.top_emotion(face)
        
        # Display the detected emotion and generate a compliment
        if emotion == 'happy':
            compliment = "Your smile is radiant!"
        elif emotion == 'neutral':
            compliment = "You have a calm presence."
        elif emotion == 'sad':
            compliment = "Don't worry, this too shall pass."
        elif emotion == 'surprise':
            compliment = "Wow, you look surprised!"
        elif emotion == 'fear':
            compliment = "Don't be scared, everything will be okay."
        else:
            compliment = "You're unique in your own way!"

        # Display the emotion and compliment on the image
        cv2.putText(frame, f"{compliment}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Show the resulting image
    cv2.imshow('Face and Emotion Detection', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
