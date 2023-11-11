import threading
import time
import cv2


def duck():
    print("kwek")
    time.sleep(1)
    print("another kwek")


# Open the webcam (the argument 0 corresponds to the default webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()


def get_frame_webcam():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()


t1 = threading.Thread(target=get_frame_webcam)
# t1.start()
get_frame_webcam()

print(f"Number of Threads : {threading.active_count()}")
