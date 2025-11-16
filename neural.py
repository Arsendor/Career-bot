from deepseek import DeepSeekAPI
from config import API_KEY
# Создаём клиент
client = DeepSeekAPI(api_key=API_KEY)  # <-- вставь сюда свой ключ

def get_ai_response(prompt: str) -> str:
    """
    Отправляет запрос к DeepSeek API и возвращает текстовый ответ.
    Работает как для профиля пользователя, так и для свободных сообщений.
    """
    try:
        # Используем метод chat_create, который доступен в новой версии DeepSeekAPI
        response = client.chat_create(
            model="gpt-5",  # или другой доступный у тебя модельный вариант
            messages=[{"role": "user", "content": prompt}]
        )

        # В зависимости от версии библиотеки текст может быть в разных полях
        if hasattr(response, "output_text"):
            return response.output_text
        elif isinstance(response, dict) and "text" in response:
            return response["text"]
        else:
            # Пробуем взять первый элемент, если возвращается список вариантов
            try:
                return response[0]["text"]
            except (TypeError, KeyError, IndexError):
                return "Извини, я не смог получить ответ."

    except Exception as e:
        # Чтобы бот не падал при ошибке
        print(f"Ошибка при обращении к DeepSeekAPI: {e}")
        return "Извини, произошла ошибка при генерации ответа."

