# # app/services/sentiment_service.py

# from transformers import pipeline

# # Load only once
# sentiment_analyzer = pipeline("sentiment-analysis")

# def analyze_sentiment(text):
#     try:
#         results = sentiment_analyzer(text[:512])
#         if isinstance(results, list) and len(results) > 0:
#             result = results[0]
#             return {
#                 "label": result.get("label", "unknown"),
#                 "score": round(result.get("score", 0), 3)
#             }
#         else:
#             return {"error": "Empty or invalid sentiment result"}
#     except Exception as e:
#         return {"error": str(e)}

from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    try:
        result = sentiment_analyzer(text[:512])[0]
        return {
            "label": result["label"],
            "score": round(result["score"], 3)
        }
    except Exception as e:
        return {"error": str(e)}