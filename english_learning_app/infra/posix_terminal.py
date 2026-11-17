import sys, select


class PosixTerminal:
    def wait_key(self, timeout: float) -> str | None:
        if select.select([sys.stdin], [], [], timeout)[0]:
            return sys.stdin.read(1)
        return None

    def read_line(self, prompt: str = "") -> str:
        return input(prompt)
