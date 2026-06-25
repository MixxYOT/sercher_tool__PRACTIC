#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENDOR_DIR="$PROJECT_DIR/vendor/linux"

cd "$PROJECT_DIR"

echo "=============================="
echo "  Оффлайн сборка..."
echo "=============================="
echo ""

VENV_DIR=".venv-build-linux"
VENV_PYTHON="$PROJECT_DIR/$VENV_DIR/bin/python"

# Проверить наличие vendor
if [ ! -d "$VENDOR_DIR" ] || [ -z "$(ls -A $VENDOR_DIR 2>/dev/null)" ]; then
    echo "[ОШИБКА] Папка vendor/linux пуста или отсутствует!"
    echo ""
    exit 1
fi

# 🔍 Функция поиска Python 3.8
find_python38() {
    local candidates=(
        # pyenv
        "$HOME/.pyenv/versions/3.8.10/bin/python3.8"
        "$HOME/.pyenv/versions/3.8.18/bin/python3.8"
        "$HOME/.pyenv/versions/3.8*/bin/python3.8"
        
        # Системные
        "/usr/bin/python3.8"
        "/usr/local/bin/python3.8"
        "/opt/python/3.8/bin/python3.8"
        
        # В PATH
        "$(which python3.8 2>/dev/null)"
        "$(which python3 2>/dev/null)"
    )
    
    for py in "${candidates[@]}"; do
        if [ -f "$py" ] && [[ "$("$py" --version 2>&1)" == *"3.8"* ]]; then
            echo "$py"
            return 0
        fi
    done
    
    return 1
}

# Проверить venv
check_venv() {
    [ -f "$VENV_PYTHON" ] || return 1
    "$VENV_PYTHON" -c "import PyInstaller" 2>/dev/null || return 1
    return 0
}

if ! check_venv; then
    echo "Создаю venv из wheels..."
    echo ""
    
    rm -rf "$VENV_DIR"
    
    # Найти Python 3.8
    PYTHON_38=$(find_python38) || {
        echo "[ОШИБКА] Python 3.8 не найден!"
        echo ""
        echo "Установите Python 3.8:"
        echo "  sudo apt install python3.8 python3.8-venv"
        echo "  или"
        echo "  pyenv install 3.8.10"
        exit 1
    }
    
    echo "Python: $PYTHON_38"
    echo "Версия: $($PYTHON_38 --version)"
    
    # Создать venv
    "$PYTHON_38" -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Установить из vendor
    echo ""
    echo "Устанавливаю зависимости из vendor/linux..."
    python -m pip install --no-index --find-links "$VENDOR_DIR" -r "$PROJECT_DIR/req.txt"
    
    echo ""
    echo "✅ Venv создан (офлайн)"
    echo ""
else
    source "$VENV_DIR/bin/activate"
    echo "✅ Venv найден"
fi

echo "Python: $(python --version)"
echo ""

# Собрать
python -m PyInstaller build.spec --clean --noconfirm

echo ""
echo "=============================="
echo "  Готово!"
echo "=============================="
echo ""
echo "  Бинарник: dist/searcher"
echo "  Запуск:   ./dist/searcher \"искомое\" ./папка"