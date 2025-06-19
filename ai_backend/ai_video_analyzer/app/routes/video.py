from flask import Blueprint, request, jsonify, current_app
from app.services.youtube_service import extract_video_id, fetch_video_details
from app.workers.tasks import process_video_task
from celery.result import AsyncResult
from app.celery_app import celery
from flask.json import jsonify

video_bp = Blueprint("video_bp", __name__)

@video_bp.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "Running ✅",
        "message": "Use /analyze/ to analyze a YouTube video"
    }), 200

@video_bp.route("/analyze/", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        task = process_video_task.delay(url)
        return jsonify({"task_id": task.id}), 202

    except Exception as e:
        current_app.logger.error(f"[ANALYZE] Failed to start task: {e}")
        return jsonify({"error": "Failed to start task", "details": str(e)}), 500


def serialize_result(result_obj):
    try:
        return result_obj if isinstance(result_obj, (dict, list, str, int, float, bool, type(None))) else str(result_obj)
    except Exception:
        return "Unserializable"
    
    
    
    


@video_bp.route("/analyze/status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    try:
        result = AsyncResult(task_id, app=celery)

        if result.ready():
            return jsonify({
                "status": result.status,
                "result": serialize_result(result.result)
            }), 200

        return jsonify({"status": result.status}), 202

    except Exception as e:
        current_app.logger.error(f"[STATUS] Failed to fetch status: {e}")
        return jsonify({"error": "Could not fetch task status"}), 500


@video_bp.route("/analyze/report/<task_id>", methods=["GET"])
def get_report(task_id):
    try:
        result = AsyncResult(task_id, app=celery)

        if result.ready():
            return jsonify({
                "report": serialize_result(result.result)
            }), 200

        return jsonify({"error": "Report not ready"}), 202

    except Exception as e:
        current_app.logger.error(f"[REPORT] Failed to fetch report: {e}")
        return jsonify({"error": "Could not fetch report", "details": str(e)}), 500
