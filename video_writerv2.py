import queue

import cv2
import ffmpegcv

import time
import multiprocessing


class VideoWriter:
    def __init__(self):
        self.qq = multiprocessing.Queue()
        self.stop_event = multiprocessing.Event()
        self.writer = None

    def write(self):
        self.writer = ffmpegcv.VideoWriter("output_video.mp4", "h264", 30)

        while not self.stop_event.is_set():
            try:
                frm = self.qq.get(timeout=1)
                self.writer.write(frm)
                print("writing...")
            except queue.Empty:
                print("waiting for frame to write...")

        self.writer.release()
        print("writer, released")

    def stop(self):
        self.stop_event.set()


if __name__ == '__main__':
    # Call freeze_support() to support freezing the script into an executable
    multiprocessing.freeze_support()

    # first process
    # Start the video writer process
    vw = VideoWriter()
    p1 = multiprocessing.Process(target=vw.write)
    p1.start()

    # second process
    # open cam
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("dead")
            break

        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.imshow(f"webcam (fps : {fps})", frame)

        # put frame into multiprocessing queue
        vw.qq.put(frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # stop writing
    vw.stop()

    # waiting for writer finished
    p1.join()
