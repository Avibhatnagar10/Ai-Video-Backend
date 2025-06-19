from transformers import pipeline

classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

def detect_hate_speech(text):
    result = classifier(text[:512])[0]
    return {
        "label": result['label'],
        "score": round(result['score'], 3)
    }
