Сборка проекта:
1. Виртуальное окружение: ```python -m venv venv``` или ```uv venv```
2. Активировать окружение:  ```.venv\Scripts\activate```
3. Установить все зависимости из файла req.txt: ```uv pip install -r req.txt```
4. Запустить сборку
Windows: ```pyinstaller --onefile --name practica_searcher src\__main__.py```
Linux: ```pyinstaller --onefile --name practica_searcher --add-data "src:src" src/__main__.py```
