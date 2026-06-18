import asyncio
from typing import Dict, List, Optional

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table

from cli import parse_args
from searcher import FileResult, search_directory

GREEN = '\033[32m'
RESET = '\033[0m'

console = Console()


async def search_with_progress(
    folder: str,
    terms: List[str],
    extensions: Optional[List[str]] = None,
) -> Dict[str, List[FileResult]]:
    """
    Ищет одно или несколько слов в папке, рисуя прогресс-бар через rich.
    Каждое слово — отдельная строка прогресса, поиск идёт параллельно.
    """
    if not terms:
        return {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        TextColumn("{task.fields[current_file]}"),
        console=console,
    ) as progress:
        task_ids = {
            term: progress.add_task(term, total=None, current_file="")
            for term in terms
        }

        def make_callback(task_id: int):
            def callback(current: int, total: int, result: FileResult) -> None:
                if progress.tasks[task_id].total != total and total > 0:
                    progress.update(task_id, total=total)
                if result.found_count > 0:
                    cf = f"[bold green]+{result.found_count}[/] {result.file_name}"
                else:
                    cf = f"[dim]{result.file_name}[/]"
                progress.update(task_id, advance=1, current_file=cf)
            return callback

        coros = [
            search_directory(
                folder,
                term,
                extensions=extensions,
                progress_callback=make_callback(task_ids[term]),
            )
            for term in terms
        ]
        results_list = await asyncio.gather(*coros)

    return dict(zip(terms, results_list))


def print_results_table(all_results: Dict[str, List[FileResult]]) -> None:
    """Печатает сводную таблицу результатов через rich."""
    table = Table(title="Результаты поиска", show_lines=False)
    table.add_column("Слово", style="cyan", no_wrap=True)
    table.add_column("Файл", style="magenta")
    table.add_column("Контекст", style="white")

    total_matches = 0
    files_with_hits: set = set()

    for term, results in all_results.items():
        for r in results:
            if r.matches:
                files_with_hits.add(r.filepath)
            for m in r.matches:
                total_matches += 1
                table.add_row(
                    m.match,
                    m.file,
                    m.context[:80],
                )

    console.print(table)
    console.print(
        f"\n[bold]Всего найдено[/] {total_matches} совпадений "
        f"[bold]в[/] {len(files_with_hits)} файлах"
    )


async def main_cli(args):
    """CLI-режим: поиск по аргументам и вывод результата."""
    print(f"Поиск \"{', '.join(args.pattern)}\" в {args.dir}...")
    if args.extensions:
        print(f"Расширения: {', '.join(args.extensions)}")
    print()
    
    all_results = await search_with_progress(
        folder=args.dir,
        terms=args.pattern,
        extensions=args.extensions
    )
    print_results_table(all_results)
    
async def main():
    args = parse_args()

    if args.pattern:
        await main_cli(args)
    else:
        raw = input("Что искать (несколько слов через пробел): ").strip()
        folder = input("Где искать: ").strip()

        if not folder.strip():
            folder = "./"

        terms = [t for t in raw.split() if t]

        if not terms:
            print("Пустой запрос")
            return

        all_results = await search_with_progress(folder, terms)
        print_results_table(all_results)


if __name__ == "__main__":
    asyncio.run(main())
