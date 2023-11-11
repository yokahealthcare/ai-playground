import cv2
import ffmpegcv
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
        self.stop_event = multiprocessing.Event()
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


class OpenCVVideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

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
        for frame in video_capture.get_frame(vwrite.qq):
            cv2.imshow("Webcam", frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Cleanup: close the OpenCV window, stop writing, and join the multiprocessing process
    cv2.destroyAllWindows()
    vwrite.stop()
    p1.join()
