import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

pipeline = Gst.Pipeline()

filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
filesrc.set_property("location", "/path/to/video.mp4")

decodebin = Gst.ElementFactory.make("decodebin", "decodebin")

videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")

x264enc = Gst.ElementFactory.make("x264enc", "x264enc")
x264enc.set_property("tune", "zerolatency")
x264enc.set_property("byte-stream", True)
x264enc.set_property("bitrate", 80000)

rtph264pay = Gst.ElementFactory.make("rtph264pay", "rtph264pay")
rtph264pay.set_property("pt", 96)

rtspclientsink = Gst.ElementFactory.make("rtspclientsink", "rtspclientsink")
rtspclientsink.set_property("location", "rtsp://<server-ip>:<port>/test")

pipeline.add(filesrc)
pipeline.add(decodebin)
pipeline.add(videoconvert)
pipeline.add(x264enc)
pipeline.add(rtph264pay)
pipeline.add(rtspclientsink)

filesrc.link(decodebin)
decodebin.link(videoconvert)
videoconvert.link(x264enc)
x264enc.link(rtph264pay)
rtph264pay.link(rtspclientsink)

pipeline.set_state(Gst.State.PLAYING)
