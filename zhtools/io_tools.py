def read_file(filename: str, offset: int, size: int) -> str:
    """Read the specified interval content of text file"""
    with open(filename, 'r') as f:
        f.seek(offset)
        return f.read(size)
