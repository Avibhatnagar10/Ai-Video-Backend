import os
import requests
from urllib.parse import urlparse, parse_qs

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    return None

def fetch_video_details(video_id):
    if not video_id:
        raise ValueError("Invalid YouTube URL or missing video ID")

    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data.get("items"):
        raise ValueError("No video data found")

    video_data = data["items"][0]
    snippet = video_data["snippet"]
    stats = video_data["statistics"]

    return {
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "channelTitle": snippet.get("channelTitle"),
        "publishedAt": snippet.get("publishedAt"),
        "viewCount": stats.get("viewCount", 0),
        "likeCount": stats.get("likeCount", 0),
        "commentCount": stats.get("commentCount", 0),
    }