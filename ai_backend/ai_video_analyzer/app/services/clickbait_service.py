def detect_clickbait(title, description):
    try:
        # Very basic keyword-based placeholder
        clickbait_keywords = ["you won’t believe", "shocking", "must see", "unbelievable"]
        content = f"{title} {description}".lower()
        score = sum(1 for word in clickbait_keywords if word in content)
        return {
            "clickbait_level": "high" if score > 1 else "low",
            "keywords_found": score
        }
    except Exception as e:
        return {"error": str(e)}