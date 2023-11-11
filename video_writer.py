import cv2
import multiprocessing
from multiprocessing import Pool
import time
import ffmpegcv


class WebcamVideoWriter:
    def __init__(self, output_path, fps, width, height, frame_queue):
        self.output_path = output_path
        self.fps = fps
        self.width = width
        self.height = height
        self.frame_queue = frame_queue
        self.video_writer = None

    def start_writing(self):
        # Define the FourCC codec and create a VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        # self.video_writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))
        self.video_writer = ffmpegcv.VideoWriter(self.output_path, 'h264', self.fps, (self.width, self.height))

        while True:
            # Check if there is a frame in the queue
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()

                # Write the frame to the video file
                self.video_writer.write(frame)
                print("writing frame...")

            # Sleep briefly to avoid busy-waiting
            time.sleep(0.01)

    def stop_writing(self):
        # Release the video writer
        if self.video_writer is not None:
            self.video_writer.release()
            print("video writer release the video")


class WebcamStreamer:
    def __init__(self, frame_queue):
        self.frame_queue = frame_queue

    def start_streaming(self):
        # Start capturing video from the webcam
        cap = cv2.VideoCapture(0)  # 0 represents the default webcam

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Display the resulting frame
            cv2.imshow('Webcam', frame)

            # Put the frame in the queue for the writing process
            self.frame_queue.put(frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam
        cap.release()

        # Notify the writing process to stop
        self.frame_queue.put(None)

        # Destroy all OpenCV windows
        cv2.destroyAllWindows()


if __name__ == "__main__":
    output_path = "output_video.mp4"
    fps = 30  # You can adjust the frames per second
    width, height = 640, 480  # You can adjust the width and height

    # Create a multiprocessing Queue for passing frames between processes
    frame_queue = multiprocessing.Queue()

    # Create instances of the WebcamStreamer and WebcamVideoWriter classes
    webcam_streamer = WebcamStreamer(frame_queue)
    webcam_writer = WebcamVideoWriter(output_path, fps, width, height, frame_queue)

    # Create separate processes for streaming and writing
    streaming_process = multiprocessing.Process(target=webcam_streamer.start_streaming)
    writing_process = multiprocessing.Process(target=webcam_writer.start_writing)

    # Start the processes
    writing_process.start()
    print("writing process running...")
    streaming_process.start()
    print("streaming process running...")


    # Wait for the streaming process to finish (when 'q' is pressed)
    print("streaming process join...")
    streaming_process.join()
    print("streaming process finished...")

    # Stop the writing process after streaming is done
    webcam_writer.stop_writing()
    print("writing process stopped...")

    # Wait for the writing process to finish
    print("writing process join...")
    writing_process.join()
    print("writing process stopped...")
