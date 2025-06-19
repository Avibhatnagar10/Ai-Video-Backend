def detect_violations(text):
    try:
        violations = []
        if any(word in text.lower() for word in ["kill", "suicide", "blood"]):
            violations.append("violent")
        if any(word in text.lower() for word in ["sex", "nude"]):
            violations.append("adult")
        return {
            "violations": violations if violations else ["none"]
        }
    except Exception as e:
        return {"error": str(e)}