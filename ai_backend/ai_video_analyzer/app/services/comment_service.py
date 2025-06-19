def analyze_comments(comments):
    try:
        from transformers import pipeline
        sentiment_analyzer = pipeline("sentiment-analysis")

        sentiments = [sentiment_analyzer(comment[:512])[0] for comment in comments]
        positive = sum(1 for s in sentiments if s["label"] == "POSITIVE")
        negative = sum(1 for s in sentiments if s["label"] == "NEGATIVE")
        neutral = len(comments) - positive - negative

        return {
            "total": len(comments),
            "positive": positive,
            "negative": negative,
            "neutral": neutral
        }
    except Exception as e:
        return {"error": str(e)}