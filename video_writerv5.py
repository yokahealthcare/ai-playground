import cv2
from tqdm import tqdm
import ffmpegcv

import os
import multiprocessing
from queue import Empty


class VideoWriter:
    def __init__(self, output_path, fps, writer_impl):
        """
        Initialize the VideoWriter.

        Args:
            output_path (str): Output path for the finished video file.
            width (int): Width of the inputted frame.
            height (int): Height of the inputted frame.
            fps (int): Frames per second for the video.
            writer_impl: Video writer implementation (e.g., ffmpegcv.VideoWriter).
        """
        self.qq = multiprocessing.Queue()
        self.output_path = output_path
        self.fps = fps
        self.writer_impl = writer_impl
        self.writer = None

    def start(self):
        """
        Start the process of writing video.

        Output:
            Video file (mp4) with codec (h264).
        """
        # Define the video writer using the provided implementation
        self.writer = self.writer_impl(self.output_path, "h264", self.fps)

        # Initiating loop for the process
        while True:
            data = self.qq.get(timeout=1)
            if data is None:
                # Release writer if stop_event is set (or occur)
                self.writer.release()
                print("Writer is released")
                return

            try:
                self.writer.write(data)
                # print("Writing...")
            except Empty:
                print("Waiting for frame to write...")


class OpenCVVideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture("assets/videos/daylight_480p.mp4")
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()

    def get_frame(self, queue):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Dead")
                break
            queue.put(frame)
            yield frame


if __name__ == "__main__":
    output_path = "output_video.mp4"
    width, height, fps = 500, 500, 20

    # Start multiprocessing for writing
    vwrite = VideoWriter(output_path, fps, ffmpegcv.VideoWriter)
    p1 = multiprocessing.Process(target=vwrite.start)
    p1.start()

    # Use 'with' statement for video capture
    with OpenCVVideoCapture() as video_capture:
        for frame in tqdm(video_capture.get_frame(vwrite.qq), total=video_capture.total_frames,
                          desc="Processing frames"):
            cv2.imshow("Webcam", frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Cleanup: close the OpenCV window, stop writing, and join the multiprocessing process
    cv2.destroyAllWindows()
    print("cv2 windows all destroyed")

    vwrite.qq.put(None)

    print("process join...")
    p1.join()
    print("process finished")
    # os._exit(0)
