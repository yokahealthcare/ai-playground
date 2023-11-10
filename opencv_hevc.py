import ffmpegcv
vidin = ffmpegcv.VideoCapture("assets/opencv/raw/capacitor.mp4")
vidout = ffmpegcv.VideoWriterNV("assets/opencv/uncompressed/capacitor-H264.mp4", 'h264', vidin.fps)

with vidin, vidout:
    for frame in vidin:
        vidout.write(frame)
