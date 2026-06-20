## 📄 Поддерживаемые форматы

| Формат | Библиотека 
|--------|-----------|
| `.docx` | python-docx | Microsoft Word 2007+ |
| `.pdf` | PyMuPDF
| `.xlsx` | openpyxl
| `.odt` | odfpy
| `.ods` | odfpy
| `.doc` | olefile
| `.txt` и другие | -

---

## Требования

- **Python 3.8.10** (протестировано на этой версии)

---

## Установка и запуск

### 1. Клонируйте репозиторий
### 2. Создайте и активируйте виртуальное окружение
##### Linux 
```bash
python -m venv venv
source venv/bin/activate
```

##### Windows
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
### 3. Установите зависимости
```bash
pip install -r req.txt
```
### 4. Запустите
```bash
python -m src <слово> -d <путь_к_папке>
```
**Примеры:**
```bash
# Поиск слова "тема" в папке docs
python src/__main__.py тема -d ./docs

# Поиск слова "отчет" в папке /home/user/documents
python src/__main__.py отчет -d /home/user/documents
```
## Сборка в исполняемый файл
Собранный файл не требует установки Python и библиотек на целевой машине.
### 1. Установите PyInstaller
```bash
pip install pyinstaller
```
### 2. Соберите проект
```bash
pyinstaller build.spec
```
### 3. Запустите собранный файл
##### Linux 
```bash
./dist/searcher <слово> -d <путь_к_папке>
```
##### Windows
```powershell
.\dist\searcher.exe <слово> -d <путь_к_папке>
```















