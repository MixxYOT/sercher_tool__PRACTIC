@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

cd /d "%~dp0\.."

echo ==============================
echo   Оффлайн сборка...
echo ==============================
echo.

set VENV_DIR=.venv-build-windows
set VENDOR_DIR=vendor\windows
set REQ_FILE=req.txt

REM Проверить наличие vendor
if not exist "%VENDOR_DIR%\" (
    echo [ОШИБКА] Папка %VENDOR_DIR% отсутствует!
    echo.
    exit /b 1
)

REM Проверить что vendor не пустая
dir /b "%VENDOR_DIR%\*.whl" >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Папка %VENDOR_DIR% пуста!
    exit /b 1
)

REM Проверить venv
if exist "%VENV_DIR%\Scripts\python.exe" (
    "%VENV_DIR%\Scripts\python.exe" -c "import PyInstaller" >nul 2>&1
    if not errorlevel 1 (
        echo Venv найден!
        call "%VENV_DIR%\Scripts\activate.bat"
        goto :build
    )
)

echo Создаю venv из wheels...
echo.

REM Удалить старый venv
if exist "%VENV_DIR%" rmdir /s /q "%VENV_DIR%"

REM Найти Python 3.8
set PYTHON_CMD=

REM Способ 1: py launcher
py -3.8 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.8
    goto :found_python
)

REM Способ 2: стандартные пути
if exist "C:\Python38\python.exe" (
    set PYTHON_CMD=C:\Python38\python.exe
    goto :found_python
)
if exist "%LOCALAPPDATA%\Programs\Python\Python38\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python38\python.exe
    goto :found_python
)
if exist "%ProgramFiles%\Python38\python.exe" (
    set PYTHON_CMD=%ProgramFiles%\Python38\python.exe
    goto :found_python
)

REM Способ 3: pyenv
if exist "%USERPROFILE%\.pyenv\pyenv-win\versions\3.8.10\python.exe" (
    set PYTHON_CMD=%USERPROFILE%\.pyenv\pyenv-win\versions\3.8.10\python.exe
    goto :found_python
)
if exist "%USERPROFILE%\.pyenv\pyenv-win\versions\3.8.18\python.exe" (
    set PYTHON_CMD=%USERPROFILE%\.pyenv\pyenv-win\versions\3.8.18\python.exe
    goto :found_python
)

REM Способ 4: в PATH
where python >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%i in ('python --version 2^>^&1') do set VER=%%i
    echo !VER! | findstr "3.8" >nul
    if not errorlevel 1 (
        set PYTHON_CMD=python
        goto :found_python
    )
)

echo [ОШИБКА] Python 3.8 не найден!
echo.
exit /b 1

:found_python
echo Python: %PYTHON_CMD%
"%PYTHON_CMD%" --version
echo.

REM Создать venv
"%PYTHON_CMD%" -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ОШИБКА] Не удалось создать venv
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"

python -m pip install --upgrade pip

REM Установить из vendor
echo.
echo Устанавливаю зависимости из %VENDOR_DIR%...
python -m pip install --no-index --find-links "%VENDOR_DIR%" -r "%REQ_FILE%"
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить зависимости
    exit /b 1
)

echo.
echo [OK] Venv создан
echo.

:build
echo Python: 
python --version
echo.

REM Собрать
python -m PyInstaller build.spec --clean --noconfirm
if errorlevel 1 (
    echo.
    echo [ОШИБКА] Сборка не удалась!
    exit /b 1
)

echo.
echo ==============================
echo   Готово!
echo ==============================
echo.
echo   Бинарник: dist\searcher.exe
echo   Запуск:   dist\searcher.exe "искомое" .\папка
echo.

endlocal