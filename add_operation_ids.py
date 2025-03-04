import yaml
import re
import sys

def generate_operation_id(http_method, path):
    """
    Генерира operationId по схема:
    - Използва името на HTTP метода (в малки букви).
    - За пътя премахва водещия "/" и го разделя на сегменти.
    - За всеки сегмент:
      - Ако е параметър (например "{id}"), генерира "by" + името на параметъра с главна първа буква.
      - В противен случай използва сегмента в малки букви.
    Пример:
      http_method="GET", path="/users/{id}"  --> "get_users_byId"
    """
    # Премахваме водещия слеш, ако има такъв
    path = path.lstrip('/')
    segments = path.split('/')
    parts = []
    for seg in segments:
        # Проверяваме дали сегментът представлява параметър
        if seg.startswith('{') and seg.endswith('}'):
            param = seg[1:-1]
            # Добавяме "by" и параметъра с първа главна буква
            parts.append("by" + param.capitalize())
        else:
            parts.append(seg.lower())
    return http_method.lower() + "_" + "_".join(parts)

def update_operation_ids(api_spec):
    """
    Обхожда всички пътища в спецификацията и за всеки HTTP метод,
    ако няма operationId, добавя го, използвайки generate_operation_id.
    """
    if 'paths' not in api_spec:
        return api_spec

    for path, methods in api_spec['paths'].items():
        for method, details in methods.items():
            # Обработваме само HTTP методи
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                if 'operationId' not in details:
                    details['operationId'] = generate_operation_id(method, path)
    return api_spec

def main(input_file, output_file):
    # Зареждаме YAML файла
    with open(input_file, 'r', encoding='utf-8') as f:
        api_spec = yaml.safe_load(f)

    # Обновяваме спецификацията
    updated_spec = update_operation_ids(api_spec)

    # Записваме обновената версия в изходния файл
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(updated_spec, f, sort_keys=False, allow_unicode=True)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python add_operation_ids.py input_file.yml output_file.yml")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
