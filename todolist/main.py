from __future__ import annotations

from todolist.cli.menu import CLI


def main() -> None:
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
