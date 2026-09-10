"""Выборочная сборка EXE: Run в PyCharm или --help в терминале."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
# Для запуска без меню впишите номера, например: ["01", "04"].
SELECTED_PROGRAMS: list[str] = []


def select_programs(value: str, programs: list[dict]) -> list[dict]:
    tokens = value.replace(",", " ").split()
    if tokens == ["all"]:
        return programs
    if not tokens:
        return []
    selected = set()
    for token in tokens:
        key = token.zfill(2)
        if key not in {p["id"] for p in programs}:
            raise ValueError(f"Неизвестный номер программы: {token}")
        selected.add(key)
    return [p for p in programs if p["id"] in selected]


def source_for(program: dict, root: Path = ROOT) -> Path:
    pattern = re.compile(r"\d+_" + re.escape(program["name"]) + r"_v(\d+)\.py")
    matches = [(int(m[1]), path) for path in root.iterdir()
               if path.is_file() and (m := pattern.fullmatch(path.name))]
    if not matches:
        raise FileNotFoundError(f"Не найден исходник {program['name']}_vN.py")
    version = max(v for v, _ in matches)
    latest = [path for v, path in matches if v == version]
    if len(latest) != 1:
        raise ValueError(f"Неоднозначная версия исходника: {latest}")
    return latest[0]


def destinations_for(program: dict, source: Path, root: Path = ROOT) -> list[Path]:
    dist = (root / "dist").resolve()
    targets = [(dist / folder / source.with_suffix(".exe").name).resolve()
               for folder in program["destinations"]]
    # Корневая копия обновляется вместе с копиями для CV и клиента.
    targets.append((dist / source.with_suffix(".exe").name).resolve())
    targets = list(dict.fromkeys(targets))
    for target in targets:
        if not target.is_relative_to(dist) or not target.parent.is_dir():
            raise ValueError(f"Недоступна целевая директория: {target.parent}")
    return targets


def deploy(artifact: Path, program: dict, targets: list[Path], backup: Path) -> None:
    """Заменить все копии; восстановить старые при ошибке удаления/копирования."""
    pattern = re.compile(r"\d+_" + re.escape(program["name"]) + r"(?:_v\d+)?\.exe", re.I)
    originals = []
    for index, target in enumerate(targets):
        for old in target.parent.iterdir():
            if old.is_file() and pattern.fullmatch(old.name):
                saved = backup / str(index) / old.name
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(old, saved)
                originals.append((old, saved))
    removed, installed = [], []
    try:
        for old, saved in originals:
            old.unlink()
            removed.append((old, saved))
        for target in targets:
            installed.append(target)
            shutil.copy2(artifact, target)
    except OSError:
        for target in installed:
            target.unlink(missing_ok=True)
        for old, saved in removed:
            shutil.copy2(saved, old)
        raise


def build(program: dict, source: Path, targets: list[Path], dry_run: bool) -> None:
    base = ROOT / "temp" / "pyinstaller" / program["id"]
    command = [sys.executable, "-m", "PyInstaller", "--onefile", "-w",
               "--noconfirm", "--clean", "--runtime-tmpdir=hi_temp",
               "--workpath", str(base / "build"), "--specpath", str(base / "spec"),
               "--distpath", str(base / "output")]
    for module in program["exclude"]:
        command.extend(["--exclude-module", module])
    if program["ui"]:
        command.extend(["--add-data", f"{ROOT / 'ui'};ui"])
    command.append(str(source))
    print(f"\n{source.name}", flush=True)
    for target in targets:
        print(f"  -> {target}", flush=True)
    if dry_run:
        print(subprocess.list2cmdline(command))
        return
    base.mkdir(parents=True, exist_ok=True)
    artifact = base / "output" / f"{source.stem}.exe"
    artifact.unlink(missing_ok=True)
    subprocess.run(command, cwd=ROOT, check=True)
    if not artifact.is_file() or artifact.stat().st_size == 0:
        raise RuntimeError(f"PyInstaller не создал EXE: {artifact}")
    # Не удаляем резервные копии при ошибке: они доступны для ручного восстановления.
    backup = Path(tempfile.mkdtemp(prefix="backup-", dir=base))
    try:
        deploy(artifact, program, targets, backup)
    except OSError as exc:
        raise RuntimeError(f"Ошибка замены EXE; закройте работающую программу. "
                           f"Резервные копии: {backup}") from exc
    shutil.rmtree(backup)
    print("Готово: все копии обновлены.", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("programs", nargs="*", help="Номера через пробел/запятую или all")
    parser.add_argument("--dry-run", action="store_true", help="Показать команды без сборки и изменений")
    args = parser.parse_args()
    programs = json.loads(Path(__file__).with_name("pyinstaller_programs.json").read_text(encoding="utf-8"))
    for program in programs:
        print(f"{program['id']}  {program['name']}")
    try:
        value = " ".join(args.programs or SELECTED_PROGRAMS)
        if not value:
            value = input("Номера через пробел/запятую; all — все; Enter — выход: ")
        selected = select_programs(value, programs)
        if not selected:
            print("Сборка отменена.")
            return 0
        if os.name != "nt" and not args.dry_run:
            raise RuntimeError("Сборку Windows EXE необходимо запускать в Windows.")
        # Проверяем все исходники и директории до начала первой сборки.
        jobs = []
        for program in selected:
            source = source_for(program)
            jobs.append((program, source, destinations_for(program, source)))
        for program, source, targets in jobs:
            build(program, source, targets, args.dry_run)
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nСборка прервана.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
