import re
import os
import time
from pathlib import Path
from gtts import gTTS
import random

def extract_terms_from_english_file(file_path):
    """Извлекает английские термины из english_terms.txt"""
    terms = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    terms.append(line)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    return terms

def extract_terms_from_dictionary(file_path):
    """Извлекает английские термины из dictionary.txt"""
    terms = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                match = re.search(r'\s*-\s*', line)
                if not match:
                    continue
                english_part = line[match.end():].strip()
                bracket_match = re.search(r'\(([^)]+)\)', english_part)
                if bracket_match:
                    cleaned = bracket_match.group(1).strip()
                    first_variant = re.split(r'[,/]', cleaned)[0].strip()
                    terms.append(first_variant)
                else:
                    first_term = re.split(r'[,/]', english_part)[0].strip()
                    terms.append(first_term)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    return terms

def generate_audio_with_retry(term, output_file, max_retries=3):
    """Генерирует аудио с повторными попытками при ошибке"""
    for attempt in range(max_retries):
        try:
            # Добавляем случайную задержку между запросами (1-3 секунды)
            time.sleep(random.uniform(1, 3))
            
            tts = gTTS(text=term, lang='en', slow=False)
            tts.save(output_file)
            return True
        except Exception as e:
            print(f"    Попытка {attempt + 1}/{max_retries} не удалась: {str(e)[:50]}...")
            if attempt < max_retries - 1:
                # Увеличиваем задержку перед следующей попыткой
                wait_time = 5 * (attempt + 1)
                print(f"    Ждём {wait_time} секунд перед повторной попыткой...")
                time.sleep(wait_time)
            else:
                print(f"    ❌ Не удалось сгенерировать {term}")
                return False
    return False

def generate_audio_for_terms(terms, output_dir, start_from=0):
    """Генерирует аудиофайлы для списка терминов с защитой от блокировки"""
    print(f"\nНачинаю генерацию {len(terms)} аудиофайлов в папку '{output_dir}'...")
    print("=" * 60)
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    successful = 0
    failed = 0
    
    for i, term in enumerate(terms):
        if i < start_from:
            continue
            
        filename = f"timbrica-speech ({i}).mp3"
        filepath = os.path.join(output_dir, filename)
        
        # Пропускаем уже существующие файлы
        if os.path.exists(filepath):
            print(f"✓ [{i+1}/{len(terms)}] {filename} уже существует, пропускаем.")
            successful += 1
            continue
        
        print(f"🎵 [{i+1}/{len(terms)}] Генерирую: {term} -> {filename}")
        
        if generate_audio_with_retry(term, filepath):
            print(f"  ✅ Сохранено")
            successful += 1
        else:
            print(f"  ❌ Пропущено: {term}")
            failed += 1
        
        # Каждые 10 файлов делаем дополнительную паузу
        if (i + 1) % 5 == 0:
            print(f"\n⏸️ Пауза 5 секунд после {i+1} файлов...")
            time.sleep(10)
    
    print("\n" + "=" * 60)
    print(f"✨ Генерация завершена!")
    print(f"   ✅ Успешно: {successful}")
    print(f"   ❌ Ошибок: {failed}")
    print(f"   📁 Файлы сохранены в: {output_dir}")
    
    # Сохраняем прогресс в файл
    progress_file = os.path.join(output_dir, "generation_progress.txt")
    with open(progress_file, 'w', encoding='utf-8') as f:
        f.write(f"Последний успешно сгенерированный индекс: {successful + failed - 1}\n")
        f.write(f"Всего терминов: {len(terms)}\n")
        f.write(f"Успешно: {successful}\n")
        f.write(f"Ошибок: {failed}\n")

def main():
    # ========== НАСТРОЙКИ ==========
    # Путь к вашей папке
    source_folder = r"C:\Users\Tixon11\Desktop\кр по англу"
    
    # С какого номера продолжить (если прервалось)
    # Например, если остановилось на 8-м, укажите 8
    start_from = 0  # <-- ИЗМЕНИТЕ ЭТО, ЕСЛИ НУЖНО ПРОДОЛЖИТЬ С ОПРЕДЕЛЁННОГО МЕСТА
    # ================================
    
    audio_output_dir = os.path.join(source_folder, "audio_terms")
    
    print("=" * 60)
    print("🎙️ АУДИО-ГЕНЕРАТОР С ЗАЩИТОЙ ОТ БЛОКИРОВОК")
    print("=" * 60)
    print(f"📁 Папка с проектом: {source_folder}")
    print(f"🎵 Папка для аудио: {audio_output_dir}")
    print(f"▶️ Начинаем с индекса: {start_from}")
    print("-" * 60)
    
    # Загружаем термины
    english_terms_path = os.path.join(source_folder, "english_terms.txt")
    
    if not os.path.exists(english_terms_path):
        print(f"\n❌ Файл english_terms.txt не найден в папке: {source_folder}")
        print("Создайте этот файл со списком терминов (по одному на строку)")
        return
    
    terms = extract_terms_from_english_file(english_terms_path)
    
    if not terms:
        print("❌ Не найдены термины в файле english_terms.txt")
        return
    
    print(f"📊 Загружено терминов: {len(terms)}")
    
    # Генерируем аудио
    generate_audio_for_terms(terms, audio_output_dir, start_from)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Генерация прервана пользователем")
        print("Чтобы продолжить с того же места, укажите start_from = индекс_последнего_успешного + 1")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("Попробуйте запустить скрипт снова - он продолжит с того же места")