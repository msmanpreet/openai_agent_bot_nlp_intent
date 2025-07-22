import spacy

nlp = spacy.load("en_core_web_sm")

INTENT_KEYWORDS = {
    "search subscriptions": ["subscription", "subscriptions", "plans", "search subscription"],
    "fetch ip details": ["ip", "ip address", "fetch ip", "ip details"]
}

def classify_intent(text: str) -> str:
    doc = nlp(text.lower())
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in doc.text for keyword in keywords):
            return intent
    return "general"