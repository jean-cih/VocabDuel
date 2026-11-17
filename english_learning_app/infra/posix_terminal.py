import sys, select
from contextlib import contextmanager
from english_learning_app.cli.display import hide_cursor, show_cursor


class PosixTerminal:
    def wait_key(self, timeout: float) -> str | None:
        if select.select([sys.stdin], [], [], timeout)[0]:
            return sys.stdin.read(1)
        return None

    def read_line(self, prompt: str = "") -> str:
        return input(prompt)

    @contextmanager
    def hidden_cursor(self) -> None:
        hide_cursor()
        try:
            yield
        finally:
            show_cursor()
