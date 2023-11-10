import os

from dotenv import load_dotenv

load_dotenv()
youtube_key = os.getenv("YOUTUBE_KEY")

from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=youtube_key)
requests = youtube.channels().list(
    part="statistics",
    forUsername='PewDiePie'
)

response = requests.execute()
print(response)
youtube.close()
