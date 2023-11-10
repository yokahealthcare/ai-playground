import tinify
tinify.key = "AickqPaMmO-sq9pmVl7HWjasosGG5BVl"

url = "https://fthmb.tqn.com/M4vd2y1a6SHUAlMYYUQExR1Jnlc=/3867x2578/filters:fill(auto,1)/Shooting-in-RAW-TIFF-JPEG-5682ac103df78ccc15bfef42.jpg"
tinify.from_url(url).to_file("assets/optimized.jpg")

