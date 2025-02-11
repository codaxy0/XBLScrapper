from datetime import datetime

from colorama import Style, init

init()


class Logging:
    def __init__(
        self,
        error_color: str = "#FF746C",
        warning_color: str = "#F8DE7E",
        info_color: str = "#6495ED",
    ) -> None:
        self.error_color = self.__hex_to_ansi(error_color)
        self.warning_color = self.__hex_to_ansi(warning_color)
        self.info_color = self.__hex_to_ansi(info_color)

    def __get_timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def __hex_to_ansi(self, hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError

        r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"

    def error(self, string: str) -> None:
        print(
            f"\033[90m[{self.__get_timestamp()}] ",
            f"{self.error_color}[error] ",
            f"\033[97m{string}",
            Style.RESET_ALL,
        )

    def warning(self, string: str) -> None:
        print(
            f"\033[90m[{self.__get_timestamp()}] ",
            f"{self.warning_color}[warning] ",
            f"\033[97m{string}",
            Style.RESET_ALL,
        )

    def info(self, string: str) -> None:
        print(
            f"\033[90m[{self.__get_timestamp()}] ",
            f"{self.info_color}[info] ",
            f"\033[97m{string}",
            Style.RESET_ALL,
        )

    @staticmethod
    def print_banner() -> None:
        print(
            Logging.__hex_to_ansi(Logging, hex_color="#6b3def"),  # type: ignore
            """
██╗  ██╗██████╗ ██╗     
╚██╗██╔╝██╔══██╗██║     
 ╚███╔╝ ██████╔╝██║     
 ██╔██╗ ██╔══██╗██║     
██╔╝ ██╗██████╔╝███████╗
╚═╝  ╚═╝╚═════╝ ╚══════╝

""",
            Style.RESET_ALL,
        )

Logging.print_banner()