import re

def extract_english_terms_from_file(input_file, output_file):
    """
    Извлекает английские термины из файла dictionary.txt
    - Берёт текст после разделителя " - "
    - Если есть скобки ( ... ), оставляет только то, что внутри скобок
    - Удаляет лишние пробелы
    """
    terms = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Ищем разделитель " - "
            match = re.search(r'\s*-\s*', line)
            if not match:
                continue
            
            # Берём правую часть (английский термин)
            english_part = line[match.end():].strip()
            
            # Ищем скобки: если есть ( ... ) или ( ... , ... ) 
            # Берём содержимое первых скобок
            bracket_match = re.search(r'\(([^)]+)\)', english_part)
            if bracket_match:
                # Если есть скобки — оставляем только то, что внутри
                cleaned = bracket_match.group(1).strip()
                # Если внутри несколько вариантов через запятую/слеш — берём первый
                first_variant = re.split(r'[,/]', cleaned)[0].strip()
                terms.append(first_variant)
            else:
                # Нет скобок — оставляем весь термин
                # Если их несколько через запятую/слеш — берём первый
                first_term = re.split(r'[,/]', english_part)[0].strip()
                terms.append(first_term)
    
    # Сохраняем результат в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        for term in terms:
            f.write(term + '\n')
    
    print(f"Обработано {len(terms)} терминов")
    print(f"Результат сохранён в {output_file}")
    return terms

# Запускаем обработку
if __name__ == "__main__":
    terms = extract_english_terms_from_file("dictionary.txt", "english_terms.txt")
    
    # Показываем первые 20 терминов для проверки
    print("\nПервые 20 терминов:")
    for i, term in enumerate(terms[:377], 1):
        print(f"{i}. {term}")