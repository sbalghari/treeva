class CommandNotFound(FileNotFoundError):
    def __init__(
        self, command, stderr=None, stdout=None, return_code=None
    ) -> None:
        self.command = command
        self.stderr = stderr
        self.stdout = stdout
        self.return_code = return_code
        msg = f"The command {self.command} not found"

        if self.stdout:
            msg += f", stdout: [{self.stdout}]"
        if self.stderr:
            msg += f", stderr: [{self.stderr}]"
        if self.return_code:
            msg += f", return code: [{self.return_code}]"

        super().__init__(msg)


class ConfigNotFound(FileNotFoundError):
    pass


class RequirementError(Exception):
    pass


class PackageError(Exception):
    pass


class Deprecated(Exception):
    pass


class ThemeConfigError(Exception):
    pass
