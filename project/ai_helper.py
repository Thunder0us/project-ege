import requests
from config import Config

def is_ollama_available():
    """Проверка доступности Ollama"""
    try:
        r = requests.get(f"{Config.OLLAMA_HOST}/api/tags", timeout=2)
        return r.status_code == 200
    except:
        return False

def explain_task(task_text: str, correct_answer: str, user_answer: str = None) -> str:
    """Получить объяснение задания"""
    if not is_ollama_available():
        return "🔴 Ollama не запущен.\n\nИспользуйте заготовленное объяснение из базы данных."
    
    prompt = f"""Ты — опытный учитель ЕГЭ. Объясни решение задания простым и понятным языком, шаг за шагом.

Задание: {task_text}
Правильный ответ: {correct_answer}
Ответ ученика: {user_answer or "Не указан"}

Дай подробное решение."""
    
    try:
        resp = requests.post(
            f"{Config.OLLAMA_HOST}/api/generate",
            json={"model": Config.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=25
        )
        return resp.json().get('response', 'Ошибка генерации ответа')
    except:
        return "Не удалось подключиться к Ollama."