import os.path
import string
import sys
from pathlib import Path
from typing import Optional


def sort_requirements(requirements: str, newline: str | None = None):
    p = Path(requirements)
    if not p.is_absolute():
        p = Path.cwd() / Path(requirements)

    items = []
    others = []
    if p.exists():
        with p.open() as f:
            for line in f.readlines():
                if line[0] in string.ascii_letters:
                    items.append(line)
                else:
                    others.append(line)

    if newline:
        if not newline.endswith("\n"):
            newline += "\n"
        items.append(newline)
    items.sort(key=lambda i: i[0].lower())

    with p.open("w") as f:
        f.writelines(others + items)


def install(pkg: str, requirements: str = "requirements.txt"):
    """install requirement and write to requirements.txt."""
    if os.system(f"pip install {pkg}"):
        return

    cmd = f"pip freeze | grep -i {pkg}"
    ret = os.popen(cmd)
    result = ret.read()
    if not result.strip():
        return

    newline = None
    for line in result.splitlines():
        if line.split("==")[0].lower() == pkg.lower():
            newline = line
            break

    if not newline:
        return

    sort_requirements(requirements, newline)


def help_info():
    """show help info"""
    for cmd, func in commands.items():
        print(cmd.ljust(10, " ") + func.__doc__)


commands = {
    "-h": help_info,
    "--help": help_info,
    "i": install,
    "install": install,
}


def execute_from_command_line(argv: Optional[list[str]] = None) -> None:
    if not argv:
        argv = sys.argv[:]

    if len(argv) == 1:
        argv.append("-h")

    assert argv[1] in commands
    cmd = commands[argv[1]]
    try:
        if len(argv) > 2:
            cmd(*argv[2:])
        else:
            cmd()
    except KeyboardInterrupt:
        pass


def main():
    execute_from_command_line()


if __name__ == "__main__":
    execute_from_command_line()
