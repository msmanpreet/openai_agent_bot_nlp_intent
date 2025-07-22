import spacy

nlp = spacy.load("en_core_web_sm")

ENV_KEYWORDS = {"prod": "prod", "production": "prod", "non-prod": "non-prod", "nonproduction": "non-prod", "uat": "uat"}

def extract_environment(text: str) -> str:
    text = text.lower()
    for key, value in ENV_KEYWORDS.items():
        if key in text:
            return value
    return ""

async def collect_parameters(message: str) -> dict:
    doc = nlp(message)
    account_name = ""
    environment = extract_environment(message)

    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "PRODUCT"]:
            account_name = ent.text
            break

    return {
        "account_name": account_name,
        "environment": environment
    }