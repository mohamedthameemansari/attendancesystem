import face_recognition
import cv2
import os

# Create a directory to store attendance records
attendance_dir = 'attendance_records'
if not os.path.exists(attendance_dir):
    os.makedirs(attendance_dir)

# Load known faces
known_faces = {}
for filename in os.listdir('attendance_images'):
    if filename.endswith('.jpg'):
        student_name = os.path.splitext(filename)[0]
        image_path = os.path.join('attendance_images', filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_faces[student_name] = encoding

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to mark attendance and exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Convert image to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations and face encodings
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Mark attendance
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = list(known_faces.keys())[first_match_index]
            # Mark attendance
            with open(os.path.join(attendance_dir, 'attendance.txt'), 'a') as f:
                f.write(f'{name}\n')
        
        # Draw rectangle around face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('Attendance System', frame)

    # Exit when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

