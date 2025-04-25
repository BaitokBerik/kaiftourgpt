# telegram_bot.py

import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from db_module import init_db, save_client, save_message
from gpt_module import ask_gpt
from config import TELEGRAM_TOKEN

# При запуске — создаём базу
init_db()

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_input = update.message.text

    print(f"[{chat_id}] {user_input}")  # лог в консоль

    # Сохраняем клиента в базу (если ещё не добавлен)
    save_client(chat_id=chat_id)

    # Сохраняем сообщение пользователя
    save_message(chat_id, "user", user_input)

    # Формируем историю диалога
    import sqlite3
    conn = sqlite3.connect("kaiftourkz.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content FROM messages
        WHERE chat_id = ?
        ORDER BY timestamp ASC
    """, (chat_id,))
    rows = cursor.fetchall()
    conn.close()

    history = [{"role": "system", "content": "Ты — эксперт по турам. Отвечай дружелюбно, уточняй детали: страна, даты, бюджет, количество человек. Не злись, не торопись."}]
    for role, content in rows:
        history.append({"role": role, "content": content})

    # Запрашиваем GPT
    gpt_reply = ask_gpt(history)

    # Сохраняем ответ
    save_message(chat_id, "assistant", gpt_reply)

    # Отправляем пользователю
    await update.message.reply_text(gpt_reply)

# Запуск бота
if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
