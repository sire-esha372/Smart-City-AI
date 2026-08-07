from textblob import TextBlob


def classify_complaint(text: str):
    text = text.lower()

    if any(word in text for word in ["garbage", "waste", "dustbin", "trash"]):
        return "Waste Management", "Municipal Sanitation"

    elif any(word in text for word in ["traffic", "signal", "jam", "vehicle"]):
        return "Traffic Management", "Traffic Department"

    elif any(word in text for word in ["electricity", "power", "current"]):
        return "Electricity", "Electricity Board"

    elif any(word in text for word in ["water", "pipe", "drain", "sewage"]):
        return "Water Supply", "Water Department"

    elif any(word in text for word in ["pollution", "smoke", "air", "noise"]):
        return "Environmental Monitoring", "Pollution Control Board"

    elif any(word in text for word in ["fire", "accident", "emergency"]):
        return "Emergency", "Emergency Response Team"

    elif any(word in text for word in ["road", "pothole"]):
        return "Road Maintenance", "Road & Infrastructure"

    elif any(word in text for word in ["street light", "light"]):
        return "Street Lights", "Electrical Maintenance"

    return "Others", "Municipal Office"


def analyze_sentiment(text: str):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "Positive"

    elif polarity < -0.2:
        return "Negative"

    return "Neutral"


def predict_priority(category, sentiment):
    if sentiment == "Negative":
        return "High"

    if category in ["Emergency", "Waste Management"]:
        return "High"

    if category in ["Traffic Management", "Road Maintenance"]:
        return "Medium"

    return "Low"


def summarize(text):
    sentences = text.split(".")
    return sentences[0]


def summarize_complaint(data):

    text = data.complaint

    category, department = classify_complaint(text)

    sentiment = analyze_sentiment(text)

    priority = predict_priority(category, sentiment)

    summary = summarize(text)

    return {
        "category": category,
        "department": department,
        "sentiment": sentiment,
        "priority": priority,
        "summary": summary
    }
    