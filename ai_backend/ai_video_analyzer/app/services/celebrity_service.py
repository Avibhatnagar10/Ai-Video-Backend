def detect_celebrities(transcript_segments):
    try:
        celebrities = ["Elon Musk", "Cristiano Ronaldo", "Taylor Swift"]
        mentions = []
        for seg in transcript_segments:
            for celeb in celebrities:
                if celeb.lower() in seg["text"].lower():
                    mentions.append({"name": celeb, "timestamp": seg["start"]})
        return mentions
    except Exception as e:
        return {"error": str(e)}