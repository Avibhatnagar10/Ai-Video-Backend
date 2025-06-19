# app/workers/tasks.py

from app.celery_app import celery
from app.services.youtube_service import extract_video_id, fetch_video_details
from app.services.transcript_service import get_transcript
from app.services.hate_speech_service import detect_hate_speech
from app.services.sentiment_service import analyze_sentiment
from app.services.clickbait_service import detect_clickbait
from app.services.content_violation_service import detect_violations
from app.services.celebrity_service import detect_celebrities
from app.services.comment_service import analyze_comments  # optional/stubbed

@celery.task(name="app.workers.tasks.process_video_task")
def process_video_task(video_url):
    try:
        # Step 1: Extract video ID
        video_id = extract_video_id(video_url)

        # Step 2: Fetch metadata
        metadata = fetch_video_details(video_id)

        # Step 3: Transcription
        transcript_data = get_transcript(video_url)
        if "error" in transcript_data:
            raise Exception(transcript_data["error"])

        full_text = transcript_data.get("full_text", "")

        # Step 4: Hate speech detection
        hate_result = detect_hate_speech(full_text) if full_text else {"label": "no_text", "score": 0}

        # Step 5: Sentiment analysis
        sentiment_result = analyze_sentiment(full_text) if full_text else {"label": "no_text", "score": 0}

        # Step 6: Clickbait analysis on title/description
        clickbait_result = detect_clickbait(metadata.get("title", ""), metadata.get("description", ""))

        # Step 7: Content violation check
        violation_result = detect_violations(full_text)

        # Step 8: Celebrity mentions
        celebrities = detect_celebrities(full_text)

        # Step 9: Comments (if needed in future)
        comments_result = analyze_comments(video_id)  # optional placeholder

        return {
            "status": "complete",
            "message": "Video processed successfully",
            "video_id": video_id,
            "video_metadata": metadata,
            "transcript": {
                "full_text": full_text,
                "segments": transcript_data.get("segments", []),
                "language": transcript_data.get("language", "unknown")
            },
            "hate_speech": hate_result,
            "sentiment": sentiment_result,
            "clickbait": clickbait_result,
            "violations": violation_result,
            "celebrities": celebrities,
            "comments": comments_result  # optional
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }
