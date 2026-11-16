import sys, termios, tty, select


class PosixTerminal:
    def wait_key(self, timeout: float) -> str | None:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)

            if select.select([sys.stdin], [], [], timeout)[0]:
                return sys.stdin.read(1)
            return None

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def read_line(self, prompt: str = "") -> str:
        return input(prompt)
