import sys, select
from contextlib import contextmanager
from english_learning_app.cli.display import hide_cursor, show_cursor
import time


class PosixTerminal:
    def wait_key(self, timeout: float | None) -> str | None:
        if select.select([sys.stdin], [], [], timeout)[0]:
            return sys.stdin.read(1)
        return None

    def wait_key_blinking(
        self,
        hint: str,
        timeout: float | None = None,
        interval: float = 0.5,
    ) -> str | None:
        deadline = None if timeout is None else time.monotonic() + timeout
        visible = True
        try:
            while True:
                line = hint if visible else " " * len(hint)
                sys.stdout.write(f"\r{line}")
                sys.stdout.flush()
                visible = not visible

                if deadline is None:
                    wait = interval
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return None
                    wait = min(interval, remaining)

                ch = self.wait_key(wait)
                if ch is not None:
                    return ch
        finally:
            sys.stdout.write(f"\r{' ' * len(hint)}\r")
            sys.stdout.flush()

    def read_line(self, prompt: str = "") -> str:
        return input(prompt)

    @contextmanager
    def hidden_cursor(self) -> None:
        hide_cursor()
        try:
            yield
        finally:
            show_cursor()
