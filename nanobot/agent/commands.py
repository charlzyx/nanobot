"""Command system for nanobot agent."""

from typing import Any, Callable
from dataclasses import dataclass
from nanobot.session.manager import Session


@dataclass
class Command:
    """A command that can be executed by the user."""

    name: str
    description: str
    handler: Callable[..., str]


class CommandRegistry:
    """Registry for user commands."""

    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}

    def register(self, command: Command) -> None:
        """Register a new command."""
        self._commands[command.name] = command

    def get(self, name: str) -> Command | None:
        """Get a command by name."""
        return self._commands.get(name)

    def list_commands(self) -> list[Command]:
        """List all registered commands."""
        return list(self._commands.values())

    def execute(self, name: str, session: Session, **kwargs: Any) -> str | None:
        """
        Execute a command.

        Args:
            name: Command name.
            session: Current session.
            **kwargs: Additional arguments.

        Returns:
            Response message, or None if command not found.
        """
        command = self.get(name)
        if command is None:
            return None
        return command.handler(session=session, **kwargs)


# Command handlers

def _reset_command(session: Session, **kwargs: Any) -> str:
    """Clear the current session history."""
    session.clear()
    return "Session reset."


def _help_command(session: Session, **kwargs: Any) -> str:
    """Show all available commands."""
    lines = ["Available commands:"]
    for cmd in default_registry.list_commands():
        lines.append(f"  /{cmd.name} - {cmd.description}")
    return "\n".join(lines)


# Default registry with built-in commands

default_registry = CommandRegistry()
default_registry.register(Command(
    name="reset",
    description="Clear the current session history",
    handler=_reset_command,
))
default_registry.register(Command(
    name="help",
    description="Show all available commands",
    handler=_help_command,
))
