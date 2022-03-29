import os.path
import string
import sys
from pathlib import Path
from typing import Optional

from zhtools.code_generator.orms import tortoise_orm, sqlalchemy_orm


ormers = {
    'tortoise': tortoise_orm,
    'sqlalchemy': sqlalchemy_orm,
}


def orm(sql: str, mode: str = 'sqlalchemy'):
    assert mode in ormers, f'mode is only in ({", ".join(ormers.keys())})'
    ormers[mode](sql)


def sort_requirements(requirements: str, newline: str = None):
    p = Path(requirements)
    if not p.is_absolute():
        p = Path.cwd() / Path(requirements)
    if not p.exists():
        return

    items = []
    others = []
    with p.open() as f:
        for line in f.readlines():
            if line[0] in string.ascii_letters:
                items.append(line)
            else:
                others.append(line)

    if newline:
        items.append(newline)
    items.sort(key=lambda i: i[0].lower())

    with p.open('w') as f:
        f.writelines(others + items)


def install(pkg: str, requirements: str = 'requirements.txt'):
    if os.system(f'pip install {pkg}'):
        return

    cmd = f'pip freeze | grep -i {pkg}'
    ret = os.popen(cmd)
    result = ret.read()
    if not result.strip():
        return

    newline = None
    for line in result.splitlines():
        if line.split('==')[0].lower() == pkg.lower():
            newline = line
            break

    if not newline:
        return

    sort_requirements(requirements, newline)


commands = {
    'orm': orm,
    'install': install,
}


def execute_from_command_line(arvg: Optional[list[str]] = None) -> None:
    if not arvg:
        arvg = sys.argv[:]

    assert arvg[0] in commands
    cmd = commands[arvg[0]]
    if len(arvg) > 1:
        cmd(*arvg[1:])
    else:
        cmd()
