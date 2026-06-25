#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "Сборка..."
echo ""

# Проверка venv
if [ ! -f ".venv-build-linux/bin/activate" ]; then
    echo "❌ Ошибка: venv не найден"
    echo "   Создайте его: python3 -m venv .venv-build-linux"
    echo "   Установите зависимости: pip install -r requirements.txt pyinstaller"
    exit 1
fi

# Активировать venv
source .venv-build-linux/bin/activate

# Собрать
python -m PyInstaller build.spec --clean

echo ""
echo "✅ Готово!"
echo "   Бинарник: dist/searcher"
echo "   Запуск: ./dist/searcher \"искомое\" ./папка"