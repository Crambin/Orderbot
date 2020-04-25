from discord.ext.commands import CheckFailure


class InvokerRoleTooLow(CheckFailure):
    def __init__(self):
        super().__init__(message="Command invoker role is lower than that of the command target's.")


class InvokerNotDeveloper(CheckFailure):
    def __init__(self):
        super().__init__(message="Command invoker is not an assigned bot developer.")
