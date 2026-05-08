import requests
from config import Config
from models import db, Task, Topic

def is_ollama_available():
    try:
        r = requests.get(f"{Config.OLLAMA_HOST}/api/tags", timeout=2)
        return r.status_code == 200
    except:
        return False

def generate_and_save_tasks(topic_id: int, count: int = 3):
    """Генерирует и сохраняет задания в базу данных"""
    if not is_ollama_available():
        return False, "❌ Ollama не запущен. Запустите Ollama и попробуйте снова."

    topic = Topic.query.get(topic_id)
    if not topic:
        return False, "Тема не найдена"

    prompt = f"""Ты — профессиональный репетитор ЕГЭ. Сгенерируй {count} качественных заданий по теме "{topic.name}" 
(предмет: {topic.subject.name}).

Для каждого задания строго соблюдай формат:

Задание: [текст задания]
Ответ: [правильный ответ]
Объяснение: [подробное решение с объяснением]

Сделай задания разного уровня сложности, соответствующие формату ЕГЭ."""

    try:
        resp = requests.post(
            f"{Config.OLLAMA_HOST}/api/generate",
            json={"model": Config.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=90
        )
        text = resp.json().get('response', '')

        tasks_added = 0
        current_task = None

        for line in text.split('\n'):
            line = line.strip()
            if line.startswith("Задание:"):
                current_task = {"text": line[8:].strip()}
            elif line.startswith("Ответ:") and current_task:
                current_task["answer"] = line[6:].strip()
            elif line.startswith("Объяснение:") and current_task:
                current_task["explanation"] = line[12:].strip()
                
                # Сохраняем задание
                if current_task.get("text") and current_task.get("answer"):
                    task = Task(
                        topic_id=topic.id,
                        text=current_task["text"],
                        correct_answer=current_task["answer"],
                        explanation=current_task.get("explanation", "Разбор от ИИ")
                    )
                    db.session.add(task)
                    tasks_added += 1
                    current_task = None

        db.session.commit()
        return True, f"✅ Успешно добавлено {tasks_added} новых заданий по теме «{topic.name}»"

    except Exception as e:
        return False, f"Ошибка связи с Ollama: {str(e)}"


def explain_with_ai(task_text: str, correct_answer: str, user_answer: str = None):
    """Получить объяснение от ИИ"""
    if not is_ollama_available():
        return "Ollama не запущен. Используйте заготовленное объяснение."

    prompt = f"""Объясни школьнику 10-11 класса решение задачи максимально понятно и дружелюбно:

Задание: {task_text}
Правильный ответ: {correct_answer}
Ответ ученика: {user_answer or "Не дан"}

Разбери шаг за шагом, используй простой язык."""
    
    try:
        resp = requests.post(
            f"{Config.OLLAMA_HOST}/api/generate",
            json={"model": Config.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=40
        )
        return resp.json().get('response', 'Не удалось получить объяснение')
    except:
        return "Не удалось подключиться к Ollama."