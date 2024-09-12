import cv2
import os

# Directory to save images
IMAGE_DIR = 'student_images'

# Create directory if it does not exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def capture_image(student_name):
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print(f"Capturing image for {student_name}. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        cv2.imshow('Capture Image', frame)
        
        # Capture image when 'c' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('c'):
            image_path = os.path.join(IMAGE_DIR, f'{student_name}.jpg')
            cv2.imwrite(image_path, frame)
            print(f"Image saved as {image_path}")
            break
        
        # Exit capture when 'q' key is pressed
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capture canceled.")
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    student_name = input("Enter student name: ")
    capture_image(student_name)
