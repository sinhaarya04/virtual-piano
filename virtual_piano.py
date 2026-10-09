import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd
import time
from pathlib import Path

class VirtualPiano:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,  # Changed to 2 to track both hands
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Piano keys configuration
        self.keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.key_width = self.width // len(self.keys)
        self.key_height = 150
        self.key_y = self.height - self.key_height

        # Audio configuration
        self.sample_rate = 44100
        self.duration = 0.3  # seconds
        self.frequencies = {
            'C': 261.63,  # C4
            'D': 293.66,  # D4
            'E': 329.63,  # E4
            'F': 349.23,  # F4
            'G': 392.00,  # G4
            'A': 440.00,  # A4
            'B': 493.88   # B4
        }

        # Key states
        self.key_states = {key: False for key in self.keys}
        self.last_played = {key: 0 for key in self.keys}
        print("Piano initialized successfully!")

    def play_note(self, note):
        try:
            current_time = time.time()
            # Add debouncing to prevent rapid retriggering
            if current_time - self.last_played[note] < 0.2:
                return

            print(f"Playing note: {note}")
            freq = self.frequencies[note]
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
            # Generate a sine wave with an amplitude envelope
            envelope = np.exp(-3 * t)
            audio_data = 0.3 * np.sin(2 * np.pi * freq * t) * envelope
            # Play the sound
            sd.play(audio_data, self.sample_rate)
            self.last_played[note] = current_time
        except Exception as e:
            print(f"Error playing note {note}: {str(e)}")

    def draw_piano(self, frame):
        # Draw piano keys
        for i, key in enumerate(self.keys):
            x = i * self.key_width
            color = (255, 255, 255) if self.key_states[key] else (0, 0, 0)
            cv2.rectangle(frame, (x, self.key_y), (x + self.key_width, self.height), color, -1)
            cv2.rectangle(frame, (x, self.key_y), (x + self.key_width, self.height), (255, 255, 255), 1)
            
            # Add key label
            label_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            label_x = x + (self.key_width - label_size[0]) // 2
            label_y = self.height - 20
            cv2.putText(frame, key, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    def is_finger_in_key(self, x, y):
        if y < self.key_y:
            return None
        
        key_index = x // self.key_width
        if 0 <= key_index < len(self.keys):
            return self.keys[key_index]
        return None

    def run(self):
        print("Virtual Piano Started!")
        print("Press 'q' to quit")
        print("You can now use both hands to play!")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Flip the frame horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)
            
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame and detect hands
            results = self.hands.process(rgb_frame)
            
            # Reset key states
            current_key_states = {key: False for key in self.keys}
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Get index fingertip coordinates (landmark 8) for each hand
                    index_finger = hand_landmarks.landmark[8]
                    x = int(index_finger.x * self.width)
                    y = int(index_finger.y * self.height)
                    
                    # Check if finger is touching a key
                    touched_key = self.is_finger_in_key(x, y)
                    if touched_key:
                        current_key_states[touched_key] = True
                        # Play sound if key wasn't pressed in previous frame
                        if not self.key_states[touched_key]:
                            self.play_note(touched_key)
            
            # Update key states
            self.key_states = current_key_states
            
            # Draw piano interface
            self.draw_piano(frame)
            
            # Display the frame
            cv2.imshow('Virtual Piano', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Clean up
        self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed successfully!")

if __name__ == "__main__":
    piano = VirtualPiano()
    piano.run() 