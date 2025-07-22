from utils.openai_client import ask_openai
from agent.parameter_collector import collect_parameters
from services.subscription_api import fetch_subscriptions
from services.ip_api import fetch_ip_details

session_data = {}

known_intents = ["search subscriptions", "fetch ip details"]

async def route_intent(message: str, session_id: str):
    if session_id not in session_data:
        session_data[session_id] = {"intent": None, "params": {}}

    session = session_data[session_id]

    if not session["intent"]:
        from nlp.intent_classifier import classify_intent
        intent = classify_intent(message)
        session["intent"] = intent

    if session["intent"] == "general":
        return await handle_general_query(message)

    session["params"].update(await collect_parameters(message))

    if "account_name" in session["params"] and "environment" in session["params"]:
        account = session["params"]["account_name"]
        env = session["params"]["environment"]

        if session["intent"] == "search subscriptions":
            result = await fetch_subscriptions(account, env)
        else:
            result = await fetch_ip_details(account, env)

        session_data.pop(session_id, None)
        return result
    else:
        missing = []
        if "account_name" not in session["params"]:
            missing.append("account name")
        if "environment" not in session["params"]:
            missing.append("environment")
        return f"Please provide the missing parameter(s): {', '.join(missing)}"

async def handle_general_query(user_input: str) -> str:
    prompt = f"""You're a helpful assistant. Answer the user's query appropriately.
    User: {user_input}
    """
    return await ask_openai(prompt)