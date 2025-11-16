import json
from neural import get_ai_response

with open("professions.json", encoding="utf-8") as f:
    PROFESSIONS = json.load(f)

def start_survey(user_data):
    user_data.clear()
    user_data["step"] = "age"
    return "Сколько тебе лет?"

def handle_survey_step(user_data, message_text):
    step = user_data.get("step")

    if step == "age":
        user_data["age"] = message_text
        user_data["step"] = "education"
        return "Какое у тебя образование?", user_data["step"]

    elif step == "education":
        user_data["education"] = message_text
        user_data["step"] = "interests"
        options = [
            "Общаться и помогать людям",
            "Работать с данными/кодом/логикой",
            "Создавать креативно",
            "Руководить и организовывать"
        ]
        return f"Что тебе нравится делать? Выбери одно или несколько:\n{', '.join(options)}", user_data["step"]

    elif step == "interests":
        user_data["interests"] = message_text
        user_data["step"] = None

        profile = get_ai_response(f"Создай короткий и дружелюбный профиль пользователя с интересами: {message_text}")
        user_data["profile"] = profile
        recommended = recommend_professions(message_text)

        return profile, recommended

    else:
        reply = get_ai_response(message_text)
        return reply, None

def recommend_professions(interests_text):
    interests_lower = interests_text.lower()
    results = []

    for p in PROFESSIONS:
        if any(interest.lower() in interests_lower for interest in p["interests"]):
            results.append({
                "title": p["title"],
                "description": p["description"],
                "link": p["link"]
            })
        if len(results) >= 5:
            break

    if not results:
        results = PROFESSIONS[:3]

    return results