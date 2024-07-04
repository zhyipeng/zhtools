class ModuleRequired(Exception):
    def __init__(self, module: str, version: str | None = None):
        self.module = module
        self.version = version

    def __str__(self) -> str:
        module = self.module
        if self.version:
            module += f">={self.version}"
        return f"Module [{module}]" f" is required. Please use pip to install it."
