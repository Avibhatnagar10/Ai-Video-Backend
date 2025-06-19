from app import create_app
from flask import jsonify

app = create_app()

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "Running ✅", "message": "Use /analyze/ to analyze a YouTube video"})

if __name__ == "__main__":
    app.run(debug=True)
