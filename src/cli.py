import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        prog='searcher',
        description='Быстрый поиск текста в офисных и текстовых файлах',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  search-tool "отчёт"                        Поиск во всех файлах текущей папки
  search-tool "тема" -d ./docs               Поиск в папке docs
  search-tool "пароль" -e .docx,.pdf,.txt    Только в указанных форматах
  search-tool "error" -i                     Без учёта регистра
  search-tool "TODO" -o results.json         Сохранить результат в JSON
        """
    )

    parser.add_argument(
        'pattern',
        nargs='*',
        help='Строка для поиска'
    )
    
    parser.add_argument(
        '-d', '--dir',
        default='.',
        help='Папка для поиска (по умолчанию: текущая)'
    )
    
    parser.add_argument(
        '-e', '--extensions',
        default=None,
        help='Расширения через запятую: .docx,.pdf,.txt (если не указано — все файлы)'
    )
    
    parser.add_argument(
        '-i', '--ignore-case',
        action='store_true',
        help='Игнорировать регистр'
    )
    
    # parser.add_argument(
    #     '-o', '--output',
    #     default=None,
    #     help='Сохранить результат в JSON-файл'
    # )
    
    parser.add_argument(
        '-w', '--whole-word',
        action='store_true',
        help='Искать только целые слова'
    )
    
    args = parser.parse_args()
    
    if args.extensions:
        args.extensions = [
            ext.strip() if ext.strip().startswith('.') else f'.{ext.strip()}'
            for ext in args.extensions.split(',')
        ]
    
    return args