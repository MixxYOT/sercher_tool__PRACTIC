@echo off
chcp 65001 >nul 2>&1
setlocal

cd /d "%~dp0\.."

echo   Сборка...
echo.

REM Проверка venv
if not exist ".venv-build-windows\Scripts\activate.bat" (
    echo [ОШИБКА] venv не найден!
    echo.
    echo   Создайте его:
    echo   python -m venv .venv-build-windows
    echo   .venv-build-windows\Scripts\activate
    echo   pip install -r requirements.txt pyinstaller
    echo.
    exit /b 1
)

REM Активировать venv
call .venv-build-windows\Scripts\activate.bat

REM Собрать
python -m PyInstaller build.spec --clean
if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Сборка не удалась!
    exit /b 1
)

echo.
echo ==============================
echo   Сборка завершена!
echo ==============================
echo.
echo   Бинарник: dist\filesearch.exe
echo   Запуск:   dist\filesearch.exe "слово" .\папка
echo.

endlocal