import cv2
import ffmpegcv
import multiprocessing
from queue import Empty


class VideoWriter:
    def __init__(self, output_path, fps):
        """
        Initialize the VideoWriter.

        Args:
            output_path (str): Output path for the finished video file.
            width (int): Width of the inputted frame.
            height (int): Height of the inputted frame.
            fps (int): Frames per second for the video.
        """
        self.stop_event = multiprocessing.Event()
        self.qq = multiprocessing.Queue()
        self.output_path = output_path
        self.fps = fps
        self.writer = None

    def start(self):
        """
        Start the process of writing video.

        Output:
            Video file (mp4) with codec (h264).
        """
        # Define the video writer
        self.writer = ffmpegcv.VideoWriter(self.output_path, "h264", self.fps)

        # Initiating loop for the process
        while not self.stop_event.is_set():
            try:
                frm = self.qq.get(timeout=1)
                self.writer.write(frm)
                print("Writing...")
            except Empty:
                print("Waiting for frame to write...")

        # Release writer if stop_event is set (or occur)
        self.writer.release()
        print("Writer is released")

    def stop(self):
        """
        Stop the writing process.
        Make the program exit the multiprocessing process.
        """
        self.stop_event.set()


def get_frame(queue):
    """
    Generator function to capture frames from the webcam.

    Args:
        queue (multiprocessing.Queue): The queue to store captured frames.

    Yields:
        numpy.ndarray: Captured frames.
    """
    cap = cv2.VideoCapture("assets/videos/daylight_480p.mp4")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Dead")
                break
            queue.put(frame)
            yield frame
    finally:
        cap.release()


if __name__ == "__main__":
    output_path = "output_video.mp4"
    width, height, fps = 500, 500, 20

    vwrite = VideoWriter(output_path, fps)

    # Start multiprocessing for writing
    p1 = multiprocessing.Process(target=vwrite.start)
    p1.start()

    try:
        # Use 'with' statement for video capture
        for frame in get_frame(vwrite.qq):
            cv2.imshow("Webcam", frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Cleanup: close the OpenCV window, stop writing, and join the multiprocessing process
        cv2.destroyAllWindows()
        vwrite.stop()
        p1.join()
