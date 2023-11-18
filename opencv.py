import cv2

# Open video file
stream = cv2.VideoCapture("assets/videos/daylight_480p.mp4")

# Check if the video stream is opened successfully
if not stream.isOpened():
    print("Error: Could not open video stream.")
    exit()

# loop over
while True:
    # read frames from stream
    ret, frame = stream.read()

    # check for frame if Nonetype
    if not ret:
        print("Error: Could not read frame.")
        break

    # {do something with the frame here}
    cv2.imshow("frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# safely close video stream
stream.release()

# safely close all OpenCV windows
cv2.destroyAllWindows()
