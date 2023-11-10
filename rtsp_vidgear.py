# import required libraries
import cv2
from vidgear.gears import CamGear
from vidgear.gears import WriteGear

# open any valid video stream(for e.g `foo.mp4` file)
stream = CamGear(source="rtsp://10.144.95.103/SP-4-MASJID-BELAKANG-1-FIGHT").start()

# define required FFmpeg parameters for your writer
output_params = {"-f": "rtsp", "-rtsp_transport": "tcp"}

# Define writer with defined parameters and RTSP address
# [WARNING] Change your RTSP address `rtsp://localhost:8554/mystream` with yours!
writer = WriteGear(
    output="rtsp://10.144.95.103:554/VIDGEAR-TESTING", logging=True, **output_params
)

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # write frame to writer
    writer.write(frame)

# safely close video stream
stream.stop()

# safely close writer
writer.close()
