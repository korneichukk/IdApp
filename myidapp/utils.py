import logging

logging.basicConfig(
    level=logging.INFO,
    format=(
        "[%(asctime)s] - [%(levelname)s]"
        " - [%(message)s] -- [%(filename)s:%(lineno)d]"
    ),
)


class logger:
    LEVEL_COLOR = {
        "debug": "\033[36m",  # CYAN
        "info": "\033[32m",  # GREEN
        "warning": "\033[33m",  # YELLOW
        "error": "\033[35m",  # MAGENTA
        "critical": "\033[31m",  # RED
        "reset": "\033[0m",  # RESET
    }

    @staticmethod
    def debug(message: str) -> None:
        logging.debug(
            f"{logger.LEVEL_COLOR.get('debug')}{message}{logger.LEVEL_COLOR.get('reset')}"
        )

    @staticmethod
    def info(message: str) -> None:
        logging.info(
            f"{logger.LEVEL_COLOR.get('info')}{message}{logger.LEVEL_COLOR.get('reset')}"
        )

    @staticmethod
    def warning(message: str) -> None:
        logging.warning(
            f"{logger.LEVEL_COLOR.get('warning')}{message}{logger.LEVEL_COLOR.get('reset')}"
        )

    @staticmethod
    def error(message: str) -> None:
        logging.error(
            f"{logger.LEVEL_COLOR.get('error')}{message}{logger.LEVEL_COLOR.get('reset')}"
        )

    @staticmethod
    def critical(message: str) -> None:
        logging.critical(
            f"{logger.LEVEL_COLOR.get('critical')}{message}{logger.LEVEL_COLOR.get('reset')}"
        )


if __name__ == "__main__":
    logger.debug("Hello, world!")
    logger.info("Hello, world!")
    logger.warning("Hello, world!")
    logger.error("Hello, world!")
    logger.critical("Hello, world!")
