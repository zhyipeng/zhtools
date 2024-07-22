from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import toml
from typer import Typer, echo

setting_file = Path('pyproject.toml')

app = Typer()


@dataclass
class Version:
    major: int = 0
    minor: int = 0
    patch: int = 0
    prerelease: int | None = None
    prefix: str = ''

    def __str__(self) -> str:
        prerelease_str = '' if self.prerelease is None else f'-{self.prerelease}'
        return f'{self.prefix}{self.major}.{self.minor}.{self.patch}{prerelease_str}'


class VersionParser:
    def __init__(self, conf: dict) -> None:
        project: dict | None = conf.get('project')
        if not project:
            conf['project'] = {}
            project = conf['project']
        self.ori = project.get('version')
        self.v = self.parse(self.ori)
        self.conf = conf

    def parse(self, v: str | None) -> Version:
        if not v:
            return Version(patch=1)

        prefix = ''
        for c in v:
            if c.isdigit():
                break
            prefix += c
        v = v.removeprefix(prefix)
        args = v.split('.')
        if len(args) != 3:
            raise ValueError(f'invalid version: {v}')

        major, minor, patch = args
        prerelease = None
        if '-' in patch:
            patch, prerelease = patch.split('-', 1)
            prerelease = int(prerelease)
        return Version(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            prerelease=prerelease,
            prefix=prefix,
        )

    def __str__(self) -> str:
        return str(self.v)

    def incr(self, tp: Literal['major', 'minor', 'patch'], pre=False) -> None:
        if pre:
            self.v.prerelease = 0
        else:
            self.v.prerelease = None

        match tp:
            case 'major':
                self.v.major += 1
                self.v.patch = 0
                self.v.minor = 0
            case 'minor':
                self.v.minor += 1
                self.v.patch = 0
            case 'patch':
                self.v.patch += 1
            case _:
                raise ValueError(f'invalid version type: {tp}')

    def prerelease(self):
        if self.v.prerelease is None:
            self.v.prerelease = 0
            self.v.patch += 1
        else:
            self.v.prerelease += 1

    def save(self):
        echo(f'new version: {self}')
        self.conf['project']['version'] = str(self)
        with setting_file.open('w') as f:
            toml.dump(self.conf, f)


def get_version():
    if not setting_file.exists():
        echo('pyproject.toml not found')
        exit(1)

    with setting_file.open('r') as f:
        conf = toml.load(f)
        return VersionParser(conf)


@app.callback(invoke_without_command=True)
def version():
    """main"""
    v = get_version()
    echo(f'current version: {v}')


@app.command()
def prerelease():
    """new pre-release version"""
    v = get_version()
    v.prerelease()
    v.save()


@app.command()
def premajor():
    """new pre-major version"""
    v = get_version()
    v.incr('major', True)
    v.save()


@app.command()
def prepatch():
    """new pre-patch version"""
    v = get_version()
    v.incr('patch', True)
    v.save()


@app.command()
def preminor():
    """new pre-minor version"""
    v = get_version()
    v.incr('minor', True)
    v.save()


@app.command()
def patch():
    """new patch version"""
    v = get_version()
    v.incr('patch')
    v.save()


@app.command()
def minor():
    """new minor version"""
    v = get_version()
    v.incr('minor')
    v.save()


@app.command()
def major():
    """new major version"""
    v = get_version()
    v.incr('major')
    v.save()
