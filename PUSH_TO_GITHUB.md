# Как запушить код в GitHub

## Вариант 1: GitHub Desktop (самый простой)

1. Скачайте и установите: https://desktop.github.com/
2. Откройте GitHub Desktop
3. File → Add Local Repository
4. Выберите папку: `D:\Чат-бот Юля\goalbuddy21`
5. Publish repository

---

## Вариант 2: Personal Access Token (через командную строку)

### Шаг 1: Создать токен

1. Откройте: https://github.com/settings/tokens
2. "Generate new token" → "Classic"
3. Выберите scope: `repo` (полный доступ к репозиториям)
4. Скопируйте токен (показывается один раз!)

### Шаг 2: Использовать токен для push

```powershell
cd "D:\Чат-бот Юля\goalbuddy21"

# Используйте токен вместо пароля:
git push https://YOUR_TOKEN@github.com/jvityazeva-gif/bot21.git main
```

Замените `YOUR_TOKEN` на ваш токен.

---

## Вариант 3: SSH ключ

### Шаг 1: Создать SSH ключ

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### Шаг 2: Добавить в GitHub

1. Скопируйте содержимое файла: `C:\Users\YOUR_USER\.ssh\id_ed25519.pub`
2. Откройте: https://github.com/settings/keys
3. "New SSH key" → вставьте ключ

### Шаг 3: Изменить remote на SSH

```powershell
cd "D:\Чат-бот Юля\goalbuddy21"
git remote set-url origin git@github.com:jvityazeva-gif/bot21.git
git push -u origin main
```

---

## Проверка репозитория

Убедитесь что репозиторий существует:
- Откройте в браузере: https://github.com/jvityazeva-gif/bot21

Если репозиторий не найден:
1. Проверьте правильность username (может быть не `jvityazeva-gif`)
2. Создайте новый репозиторий на: https://github.com/new
   - Имя: `bot21`
   - **НЕ** добавляйте README, .gitignore, license


