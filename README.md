# KaifTourGPT

🧳 Telegram-бот для подбора туров с использованием GPT-4o и SQLite.

## Возможности
- Поддержка диалога с GPT-4o
- Хранение переписки и параметров клиента
- Подготовка к интеграции с Tourvisor API
- Ведение истории общения

## Запуск
```bash
pip install -r requirements.txt
python telegram_bot.py

## Настройка

1. Скопируй `config_template.py` в `config.py`
2. Вставь свои ключи:
   - OpenAI API Key
   - Telegram Bot Token
3. Всё! Теперь можешь запускать `telegram_bot.py`