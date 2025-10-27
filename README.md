# 🤖 GoalBuddy21 - Telegram Bot

**GoalBuddy21** — чат-бот для трёхдневного интенсива в Школе 21, помогающий участникам ставить цели, отслеживать прогресс и получать поддержку.

## 🎯 Основные возможности

- **День 1**: Постановка личной цели обучения
- **День 2**: Автоматическое напоминание с проверкой прогресса
- **День 3**: Самооценка достижения цели (0-100%)
- **Интеграция с Google Sheets**: Все данные сохраняются для анализа фасилитаторами

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/jvityazeva-gif/bot21.git
cd bot21
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка конфигурации

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Заполните `.env` файл:

```env
BOT_TOKEN=ваш_токен_от_BotFather
SPREADSHEET_ID=id_вашей_google_таблицы
CREDENTIALS_PATH=credentials/google_credentials.json
SCHEDULER_TIMEZONE=Europe/Moscow
LOG_LEVEL=INFO
TESTING_MODE=True
```

### 5. Настройка Google Sheets API

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Sheets API
3. Создайте Service Account
4. Скачайте JSON ключ и сохраните как `credentials/google_credentials.json`
5. Предоставьте доступ Service Account к вашей Google таблице

### 6. Запуск бота

```bash
python run.py
```

Или используйте batch файл (Windows):
```bash
start_bot.bat
```

## 📋 Структура проекта

```
goalbuddy21/
├── bot/
│   ├── handlers.py      # Обработчики команд и сообщений
│   ├── keyboards.py     # Клавиатуры Telegram
│   ├── messages.py      # Шаблоны сообщений
│   ├── states.py        # FSM состояния
│   └── main.py          # Точка входа
├── config/
│   └── settings.py      # Настройки приложения
├── database/
│   └── sheets.py        # Работа с Google Sheets
├── scheduler/
│   └── tasks.py         # Планировщик задач
├── utils/
│   ├── logger.py        # Логирование
│   └── validators.py    # Валидация данных
├── .env.example         # Пример конфигурации
├── requirements.txt     # Зависимости
└── run.py              # Скрипт запуска
```

## 🛠 Технологический стек

- **Python 3.13**
- **python-telegram-bot 22.5** - Telegram Bot API
- **gspread 5.12** - Google Sheets интеграция
- **APScheduler 3.10** - Планировщик задач
- **oauth2client 4.1** - Аутентификация Google

## 📊 Структура данных Google Sheets

### Лист "UserData"

| Столбец | Описание |
|---------|----------|
| user_id | Telegram ID пользователя |
| username | @username |
| full_name | Имя пользователя |
| goal_text | Текст цели |
| goal_date | Дата постановки цели |
| progress_day2 | Ответ на День 2 |
| progress_date | Дата ответа День 2 |
| final_percent | Финальная оценка (0-100%) |
| final_date | Дата финальной оценки |
| current_state | Текущий статус |

## 🧪 Режим тестирования

Установите `TESTING_MODE=True` в `.env` для:
- Сокращения задержки напоминания с 24 часов до 1 минуты
- Быстрого тестирования всех функций

## 📝 Команды бота

- `/start` - Начать работу и поставить цель
- `/assess` - Оценить свой прогресс (0-100%)

## 🚂 Деплой на Railway

### Быстрый старт

1. Создайте аккаунт: https://railway.app/
2. Подключите GitHub репозиторий
3. Railway автоматически обнаружит `Dockerfile`
4. Настройте переменные окружения (см. `.env.example`)
5. Деплой!

**Подробная инструкция**: См. [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

### Локальное тестирование Docker

```bash
# Сборка образа
docker build -t goalbuddy21 .

# Запуск контейнера
docker run --env-file .env -v ./credentials:/app/credentials goalbuddy21
```

Или используйте готовый скрипт:
```bash
# Windows
.\docker-test.ps1

# Linux/Mac
./docker-test.sh
```

## 🔐 Безопасность

⚠️ **Важно**: Никогда не коммитьте в Git:
- `.env` файл (содержит токены)
- `credentials/` директорию (Google API ключи)
- `logs/` директорию

Для Railway используйте переменные окружения!

## 📄 Лицензия

MIT License

## 👥 Авторы

Разработано для Школы 21

---

## 📚 Дополнительные ресурсы

- **Railway Deploy Guide**: [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Google Sheets API**: https://developers.google.com/sheets/api

