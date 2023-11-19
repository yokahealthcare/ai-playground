import cv2
from tqdm import tqdm
import ffmpegcv

import multiprocessing
from multiprocessing import Process, Queue

FPS_DEFAULT = 25
WRITER_DEFAULT = ffmpegcv.VideoWriter


class NewVideoWriter(Process):
    def __init__(self, output_path, fps=FPS_DEFAULT, writer_impl=WRITER_DEFAULT):
        Process.__init__(self)
        self.writer = None
        self.qq = Queue()
        self.output_path = output_path
        self.fps = fps
        self.writer_impl = writer_impl

    def run(self):
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
                self.writer.write(data)
            except Exception as e:
                print("Error writing video")
                print(f"{e}")
                return


class OpenCVVideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture("assets/videos/daylight_480p.mp4")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        while True:
            ret, frm = self.cap.read()
            if not ret:
                print("\nframe break\n")
                break
            yield frm


if __name__ == "__main__":
    # Call freeze_support() to support freezing the script into an executable
    multiprocessing.freeze_support()

    video_capture = OpenCVVideoCapture()
    video_fps = video_capture.fps

    output_path = "output_video.mp4"
    p1 = NewVideoWriter(output_path, video_fps, ffmpegcv.VideoWriter)
    p1.start()

    # Use 'with' statement for video capture
    with video_capture:
        for frame in video_capture.get_frame():
            p1.qq.put(frame)

    p1.qq.put(None)
    p1.join()
