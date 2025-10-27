# 🔐 Настройка Google Credentials для Railway

## Проблема

Railway не имеет доступа к файлу `credentials/google_credentials.json` из вашего локального проекта. Нужно передать credentials через переменную окружения.

---

## Решение: Переменная окружения GOOGLE_CREDENTIALS

### Шаг 1: Откройте файл credentials

Откройте файл `credentials/google_credentials.json` в любом текстовом редакторе.

Вы увидите JSON примерно такого вида:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
```

### Шаг 2: Скопируйте ВЕСЬ JSON

**Важно:**
- Скопируйте **ВЕСЬ** содержимое файла (включая фигурные скобки)
- **НЕ** форматируйте - копируйте как есть
- Сохраните в буфер обмена

### Шаг 3: Добавьте в Railway

1. Откройте ваш проект в Railway Dashboard
2. Перейдите в **Variables** (вкладка слева)
3. Нажмите **+ New Variable**
4. **Variable Name**: `GOOGLE_CREDENTIALS`
5. **Value**: Вставьте весь скопированный JSON
6. Нажмите **Add**

### Пример (укороченный):

```
GOOGLE_CREDENTIALS={"type":"service_account","project_id":"your-project",...}
```

---

## Другие обязательные переменные

Убедитесь что добавлены все переменные:

```env
BOT_TOKEN=ваш_токен_от_BotFather
SPREADSHEET_ID=id_вашей_google_таблицы
GOOGLE_CREDENTIALS={"type":"service_account",...весь JSON...}
SCHEDULER_TIMEZONE=Europe/Moscow
LOG_LEVEL=INFO
TESTING_MODE=False
```

---

## Проверка

После добавления переменных:

1. Railway автоматически перезапустит проект
2. Откройте **Deployments** → **Logs**
3. Вы должны увидеть:

```
GoalBuddy21 - Telegram Bot
==================================================
✅ Successfully connected to Google Sheets
✅ Scheduler started
✅ Bot is ready and polling for updates...
```

---

## Если всё ещё ошибка

### Ошибка: "FileNotFoundError: credentials/google_credentials.json"

**Причина**: Переменная `GOOGLE_CREDENTIALS` не установлена или содержит некорректный JSON.

**Решение**:
1. Проверьте что переменная называется **EXACTLY** `GOOGLE_CREDENTIALS` (с учётом регистра)
2. Проверьте что JSON валидный (можно проверить на https://jsonlint.com/)
3. Убедитесь что скопировали **весь** файл, включая `{` и `}`

### Ошибка: "Invalid JSON"

**Причина**: JSON содержит ошибки или был изменён при копировании.

**Решение**:
1. Скопируйте файл заново
2. Проверьте что все кавычки и скобки на месте
3. Не добавляйте пробелы или переносы строк

---

## Альтернативный способ (Railway CLI)

Если у вас установлен Railway CLI:

```bash
cd "D:\Чат-бот Юля\goalbuddy21"

# Загрузить credentials как переменную
railway variables set GOOGLE_CREDENTIALS="$(cat credentials/google_credentials.json | tr -d '\n\r')"
```

---

## Безопасность

⚠️ **Важно**:
- Никогда не публикуйте credentials в Git
- Не делитесь скриншотами с credentials
- Railway хранит переменные в зашифрованном виде

---

## Готово!

После правильной настройки переменных бот запустится автоматически и начнёт работать! 🚀

