from flask import Blueprint, request, jsonify, current_app, send_file
from celery.result import AsyncResult
from app.services.youtube_service import extract_video_id, fetch_video_details
from app.workers.tasks import process_video_task
from app.celery_app import celery
import os
import json

video_bp = Blueprint("video_bp", __name__)

# Health check route
@video_bp.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "Running ✅",
        "message": "Use /analyze/ to analyze a YouTube video"
    }), 200

# Start video analysis
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

# Get task status
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

# Get report inline
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

# Export report as downloadable JSON file
@video_bp.route("/analyze/export/<task_id>", methods=["GET"])
def export_report(task_id):
    try:
        result = AsyncResult(task_id, app=celery)

        if result.ready():
            data = serialize_result(result.result)

            # Use absolute path based on current project directory
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../downloads"))
            os.makedirs(base_path, exist_ok=True)

            filename = f"{task_id}_report.json"
            filepath = os.path.join(base_path, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return send_file(filepath, as_attachment=True)

        return jsonify({"error": "Report not ready"}), 202

    except Exception as e:
        current_app.logger.error(f"[EXPORT] Failed to export report: {e}")
        return jsonify({"error": "Could not export report", "details": str(e)}), 500


# Safe serializer for Celery results
def serialize_result(result_obj):
    try:
        if isinstance(result_obj, (dict, list, str, int, float, bool, type(None))):
            return result_obj
        return str(result_obj)
    except Exception:
        return "Unserializable"
