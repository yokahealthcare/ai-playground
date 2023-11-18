# import required libraries
import cv2
from vidgear.gears import CamGear
from vidgear.gears import WriteGear

# open any valid video stream(for e.g `foo.mp4` file)
# stream = CamGear(source="assets/videos/daylight_480p.mp4").start()
stream = cv2.VideoCapture("assets/videos/daylight_480p.mp4")

# Check if the video stream is opened successfully
if not stream.isOpened():
    print("Error: Could not open video stream.")
    exit()

# define required FFmpeg parameters for your writer
output_params = {
    "-f": "rtsp",
    "-rtsp_transport": "tcp",
    "-vcodec": "mpeg4"
}


# Define writer with defined parameters and RTSP address
# [WARNING] Change your RTSP address `rtsp://localhost:8554/mystream` with yours!
writer = WriteGear(
    output="rtsp://10.144.95.103:554/SP-2121-WINS-CAMERA-AI", logging=True, **output_params
)

# loop over
while True:
    # read frames from stream
    ret, frame = stream.read()

    # check for frame if Nonetype
    if not ret:
        print("Error: Could not read frame.")
        break

    # {do something with the frame here}


    # Convert BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow("frame", frame)

    # writer.write(frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# safely close video stream
stream.release()

# safely close all OpenCV windows
cv2.destroyAllWindows()

writer.close()

