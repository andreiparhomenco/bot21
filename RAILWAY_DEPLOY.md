# 🚂 Деплой GoalBuddy21 на Railway

## Подготовка

### 1. Создайте аккаунт на Railway
- Перейдите: https://railway.app/
- Войдите через GitHub

---

## Деплой через GitHub (рекомендуется)

### Шаг 1: Подготовка репозитория

Убедитесь, что все коммиты запушены:
```bash
git add .
git commit -m "Add Docker support for Railway"
git push origin main
```

### Шаг 2: Создание проекта на Railway

1. Откройте: https://railway.app/new
2. Выберите "Deploy from GitHub repo"
3. Выберите репозиторий: `andreiparhomenco/bot21`
4. Railway автоматически обнаружит `Dockerfile`

### Шаг 3: Настройка переменных окружения

В Railway Dashboard → Variables, добавьте:

```env
BOT_TOKEN=ваш_токен_от_BotFather
SPREADSHEET_ID=id_вашей_google_таблицы
SCHEDULER_TIMEZONE=Europe/Moscow
LOG_LEVEL=INFO
TESTING_MODE=False
```

### Шаг 4: Загрузка Google Credentials

**Вариант A: Через переменную окружения (рекомендуется)**

1. Откройте ваш файл `credentials/google_credentials.json`
2. Скопируйте **весь JSON** в одну строку
3. В Railway Variables добавьте:
   ```
   GOOGLE_CREDENTIALS={"type":"service_account","project_id":"...",...}
   ```

4. Обновите `config/settings.py` чтобы читать из переменной:

```python
import os
import json
from pathlib import Path

# ... existing code ...

# Try to load from environment variable first (for Railway)
if os.getenv("GOOGLE_CREDENTIALS"):
    credentials_data = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    CREDENTIALS_PATH = "/tmp/google_credentials.json"
    Path(CREDENTIALS_PATH).parent.mkdir(exist_ok=True)
    with open(CREDENTIALS_PATH, 'w') as f:
        json.dump(credentials_data, f)
else:
    CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH", "credentials/google_credentials.json")
```

**Вариант B: Через Railway Volume (более сложный)**

1. В Railway создайте Volume
2. Смонтируйте в `/app/credentials`
3. Загрузите файл вручную через Railway CLI

---

## Деплой через Railway CLI

### Установка CLI

```bash
npm install -g @railway/cli
```

### Логин

```bash
railway login
```

### Инициализация проекта

```bash
cd "D:\Чат-бот Юля\goalbuddy21"
railway init
```

### Загрузка переменных

```bash
railway variables set BOT_TOKEN=ваш_токен
railway variables set SPREADSHEET_ID=ваш_id
railway variables set SCHEDULER_TIMEZONE=Europe/Moscow
railway variables set LOG_LEVEL=INFO
railway variables set TESTING_MODE=False
```

### Деплой

```bash
railway up
```

---

## Проверка работы

### Просмотр логов

В Railway Dashboard:
- Перейдите в Deploy → Logs
- Или через CLI: `railway logs`

Вы должны увидеть:
```
GoalBuddy21 - Telegram Bot
✅ Successfully connected to Google Sheets
✅ Scheduler started
✅ All handlers registered
✅ Bot is ready and polling for updates...
```

### Тестирование

1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте `/start`
4. Проверьте что данные сохраняются в Google Sheets

---

## Важные замечания

### 🔴 Для продакшена:

1. **Отключите тестовый режим**:
   ```
   TESTING_MODE=False
   ```
   Это установит задержку напоминаний на 24 часа (вместо 1 минуты)

2. **Настройте уровень логирования**:
   ```
   LOG_LEVEL=INFO
   ```
   Или `WARNING` для меньшего количества логов

3. **Мониторинг**: Railway показывает:
   - CPU/Memory usage
   - Логи в реальном времени
   - Статистику деплоев

### 💰 Стоимость

Railway предоставляет:
- **$5/месяц бесплатно** (хватит для небольшого бота)
- Далее: $0.000463/GB-hour (память) + $0.000231/vCPU-hour

Для этого бота: **~$3-5/месяц** в продакшене

---

## Устранение проблем

### Бот не запускается

1. Проверьте логи: `railway logs`
2. Убедитесь что все переменные установлены
3. Проверьте что Google credentials загружены

### "Google credentials not found"

Используйте переменную окружения `GOOGLE_CREDENTIALS` (см. выше)

### Ошибки с timezone

Установите:
```
SCHEDULER_TIMEZONE=Europe/Moscow
```

---

## Автоматические деплои

Railway автоматически делает деплой при каждом push в `main`:

```bash
git add .
git commit -m "Update bot"
git push origin main
```

Railway автоматически:
1. Соберёт новый Docker образ
2. Задеплоит
3. Перезапустит бота

---

## Полезные команды

```bash
# Логи в реальном времени
railway logs

# Статус проекта
railway status

# Открыть Dashboard
railway open

# Список переменных
railway variables

# Остановить проект
railway down
```

---

## Ссылки

- **Railway Dashboard**: https://railway.app/dashboard
- **Railway Docs**: https://docs.railway.app/
- **Telegram Bot API**: https://core.telegram.org/bots/api

