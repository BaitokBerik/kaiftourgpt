# main.py

from gpt_module import ask_gpt
from db_module import init_db, save_client, save_message

if __name__ == "__main__":
    # Инициализируем базу данных
    init_db()

    # Примерный ID пользователя (пока тестовый)
    chat_id = 123456  # В реальном боте сюда будет приходить Telegram chat_id

    # Мини-опрашиваем пользователя
    print("💬 Введи страну назначения:")
    country = input("> ")

    print("💬 Введи дату начала поездки (YYYY-MM-DD):")
    date_from = input("> ")

    print("💬 Введи дату окончания поездки (YYYY-MM-DD):")
    date_to = input("> ")

    print("💬 Введи бюджет в тенге:")
    budget = input("> ")

    print("💬 Сколько взрослых?")
    adults = input("> ")

    print("💬 Сколько детей?")
    children = input("> ")

    print("💬 Как тебя зовут?")
    name = input("> ")

    # Сохраняем профиль клиента в базу
    save_client(
        chat_id=chat_id,
        name=name,
        country=country,
        date_from=date_from,
        date_to=date_to,
        budget=int(budget),
        adults=int(adults),
        children=int(children)
    )

    print("\n✅ Профиль сохранён! Теперь напиши сообщение для бота:")

    user_input = input("> ")

    # Сохраняем сообщение пользователя
    save_message(chat_id, "user", user_input)

    # Формируем историю общения для GPT
    history = [
        {"role": "system", "content": "Ты — эксперт по подбору туров. Уточняй страну, даты, бюджет, количество человек. Будь дружелюбным, с лёгким юмором."},
        {"role": "user", "content": user_input}
    ]

    # Отправляем запрос к GPT
    gpt_reply = ask_gpt(history)

    print(f"\n🤖 GPT отвечает:\n{gpt_reply}")

    # Сохраняем ответ ассистента
    save_message(chat_id, "assistant", gpt_reply)