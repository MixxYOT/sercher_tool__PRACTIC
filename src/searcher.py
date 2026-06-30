import asyncio
from pathlib import Path
from dataclasses import dataclass, field
import re
from typing import List
from src.extractors import extract_text

# ====== ТИПЫ ======

@dataclass
class SearchMatch:
    """Одно совпадение в файле"""
    match: str          # найденная строка
    context: str        # текст вокруг (100 символов)


@dataclass
class FileResult:
    """Результат поиска в файле"""
    filepath: Path
    matches: List[SearchMatch] = field(default_factory=list)
    
    @property
    def found_count(self) -> int:
        return len(self.matches)
    
    @property
    def file_name(self) -> str:
        return self.filepath.name
    
    @property
    def directory(self) -> str:
        return str(self.filepath.parent)


# ====== ПОИСК ======

async def search_in_file(
    filepath: Path,
    search_term: str,
    ignore_case: bool = False,
    whole_word: bool = False
    ) -> FileResult:
    """
    Ищет строку в одном файле
    """
    result = FileResult(filepath=filepath)
    
    try:
        # Извлекаем текст
        loop = asyncio.get_event_loop()
        is_success, text = await loop.run_in_executor(None, extract_text, str(filepath))        

        if not is_success:
            # print(text)
            return result

        if not text.strip():
            return result
        
        
        flags = re.IGNORECASE if ignore_case else 0
        pattern_str = re.escape(search_term)
        
        if whole_word:
            pattern_str = rf'\b{pattern_str}\b'
        pattern = re.compile(pattern_str, flags)
        
        # Разбиваем на строки и ищем
        lines = text.split('\n')
        
        for i, line in enumerate(lines, 1):
            match_obj = pattern.search(line)
            if match_obj:
                # Находим позицию совпадения
                pos = match_obj.start()
                match_len = match_obj.end() - pos
                
                # Берём контекст (±50 символов вокруг)
                start = max(0, pos - 50)
                end = min(len(line), pos + match_len + 50)
                context = line[start:end].strip()
                
                match = SearchMatch(
                    match=match_obj.group(),
                    context=f"...{context}..." if start > 0 or end < len(line) else context,
                )
                result.matches.append(match)
    
    except Exception as e:
        print(f"\033[91m[Критическая ошибка поиска в файле: {e}]\033[0m")
    
    return result

async def search_directory(
    root_dir: str,
    search_term: str,
    extensions: list = None,
    progress_callback=None,
    ignore_case: bool = False,
    whole_word: bool = False
) -> List[FileResult]:
    """
    Асинхронный поиск по всем файлам в папке.
    progress_callback — функция для обновления UI (опционально).
    """
    if extensions is None:
        # extensions = ['.docx', '.doc', '.pdf', '.xlsx', '.odt', '.ods', '.txt']
        SKIP = {'.exe', '.dll', '.bin', '.dat', '.sys', '.pyc',
            '.mp3', '.mp4', '.avi', '.mov', '.mkv',
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',
            '.zip', '.7z', '.rar', '.tar', '.gz'}
    
        files = [
            f for f in Path(root_dir).rglob('*')
            if f.is_file() and f.suffix.lower() not in SKIP
        ]

    else: 
        # Собираем список файлов
        files = []
        root = Path(root_dir)
        for ext in extensions:
            files.extend(root.rglob(f"*{ext}"))
    
    results = []
    total = len(files)
    
    for i, filepath in enumerate(files, 1):
        result = await search_in_file(filepath, search_term, ignore_case, whole_word)
        results.append(result)
        
        # Отправляем прогресс в UI
        if progress_callback:
            progress_callback(i, total, result)
    
    return results
