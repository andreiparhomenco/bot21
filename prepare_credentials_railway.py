#!/usr/bin/env python3
"""
Скрипт для подготовки Google Credentials для Railway
Выводит JSON в формате, готовом для копирования в Railway Variables
"""

import json
import sys

def prepare_credentials_for_railway(input_file: str):
    """
    Читает credentials файл и выводит в формате для Railway
    """
    try:
        # Читаем оригинальный файл
        with open(input_file, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        # Преобразуем в компактный JSON (одна строка)
        compact_json = json.dumps(credentials, separators=(',', ':'), ensure_ascii=False)
        
        print("\n" + "="*80)
        print("✅ Google Credentials готовы для Railway!")
        print("="*80)
        print("\nИнструкция:")
        print("1. Откройте Railway Dashboard → Variables")
        print("2. Создайте переменную: GOOGLE_CREDENTIALS")
        print("3. Скопируйте и вставьте JSON ниже (БЕЗ кавычек в начале и конце)")
        print("\n" + "-"*80)
        print("\nJSON для копирования:\n")
        print(compact_json)
        print("\n" + "-"*80)
        print(f"\n📊 Длина JSON: {len(compact_json)} символов")
        print(f"📧 Client email: {credentials.get('client_email', 'N/A')}")
        print(f"🔑 Project ID: {credentials.get('project_id', 'N/A')}")
        print("\n✅ Готово! Скопируйте JSON и добавьте в Railway.")
        print("="*80 + "\n")
        
        # Дополнительно: валидация
        if 'type' not in credentials or credentials['type'] != 'service_account':
            print("⚠️  ВНИМАНИЕ: Это не service account credentials!")
        
        if 'private_key' not in credentials:
            print("⚠️  ВНИМАНИЕ: Отсутствует private_key!")
        
        if 'client_email' not in credentials:
            print("⚠️  ВНИМАНИЕ: Отсутствует client_email!")
            
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{input_file}' не найден!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка: Невалидный JSON в файле '{input_file}'")
        print(f"   Детали: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    input_file = "credentials/google_credentials.json"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    prepare_credentials_for_railway(input_file)

