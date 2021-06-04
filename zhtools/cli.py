from zhtools.code_generator.orms import tortoise_orm, sqlalchemy_orm


ormers = {
    'tortoise': tortoise_orm,
    'sqlalchemy': sqlalchemy_orm,
}


def orm(sql: str, mode: str = 'sqlalchemy'):
    assert mode in ormers, f'mode is only in ({", ".join(ormers.keys())})'
    ormers[mode](sql)


commands = {
    'orm': orm,
}


def execute_from_command_line(arvg=None) -> None:
    if not arvg:
        return

    assert arvg[0] in commands
    cmd = commands[arvg[0]]
    if len(arvg) > 1:
        cmd(*arvg[1:])
    else:
        cmd()
