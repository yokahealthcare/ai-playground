import cv2
from tqdm import tqdm
import ffmpegcv

import multiprocessing
from multiprocessing import Process, Queue

# Settings for writer
FPS_DEFAULT = 25
WRITER_DEFAULT = ffmpegcv.VideoWriter


class NewVideoWriter(Process):
    """A multiprocessing Process for writing video frames.

    Args:
        output_path (str): The path to the output video file.
        fps (int): Frames per second for the output video (default: 25).
        writer_impl (class): The video writer implementation (default: ffmpegcv.VideoWriter).

    Attributes:
        writer (ffmpegcv.VideoWriter): The video writer instance.
        qq (multiprocessing.Queue): A multiprocessing Queue for communication.
        output_path (str): The path to the output video file.
        fps (int): Frames per second for the output video.
        writer_impl (class): The video writer implementation.

    Methods:
        run(): The main execution method for the multiprocessing Process.
    """
    def __init__(self, output_path, fps=FPS_DEFAULT, writer_impl=WRITER_DEFAULT):
        Process.__init__(self)
        self.writer = None
        self.qq = Queue()
        self.output_path = output_path
        self.fps = fps
        self.writer_impl = writer_impl

    def run(self):
        """The main execution method for the multiprocessing Process.

        This method initializes the video writer and writes frames to the output video.
        """
        # Define the video writer using the provided implementation
        self.writer = self.writer_impl(self.output_path, "h264", self.fps)

        # Initiating loop for the process
        for _ in tqdm(iterable=iter(int, 1), desc="Video Writing Process", unit=" frame", leave=False):
            data = self.qq.get(timeout=1)
            if data is None:
                # Release writer if stop_event is set (or occur)
                self.writer.release()
                print("\nDone.\n")
                return

            try:
                # Write frame to writer
                self.writer.write(data)
            except Exception as e:
                print("Error writing video")
                print(f"{e}")
                return


class OpenCVVideoCapture:
    """A context manager for OpenCV video capture.

    Attributes:
        cap (cv2.VideoCapture): The OpenCV VideoCapture instance.
        fps (int): Frames per second of the input video.
        total_frames (int): Total number of frames in the input video.

    Methods:
        __enter__(): Enter the context (used with 'with' statement).
        __exit__(exc_type, exc_value, traceback): Exit the context (used with 'with' statement).
        get_frame(): Generator function to yield frames from the input video.
    """
    def __init__(self):
        self.cap = cv2.VideoCapture("assets/videos/daylight_480p.mp4")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __enter__(self):
        """Enter the context (used with 'with' statement)."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context (used with 'with' statement)."""
        self.cap.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        """Generator function to yield frames from the input video."""
        while True:
            ret, frm = self.cap.read()
            if not ret:
                print("\nframe break\n")
                break
            yield frm


if __name__ == "__main__":
    # Call freeze_support() to support freezing the script into an executable
    # For windows only
    multiprocessing.freeze_support()

    # Open VideoCapture OpenCV class
    video_capture = OpenCVVideoCapture()
    # Get fps value
    video_fps = video_capture.fps

    # Starting multiprocessing
    output_path = "output_video.mp4"
    p1 = NewVideoWriter(output_path, video_fps, ffmpegcv.VideoWriter)
    p1.start()

    # Use 'with' statement for video capture
    with video_capture:
        for frame in video_capture.get_frame():
            # Inject frame to multiprocessing.Queue inside the object
            p1.qq.put(frame)

    # Inject None for terminating multiprocessing process
    p1.qq.put(None)
    # Waiting for process to finish, then exit
    p1.join()
