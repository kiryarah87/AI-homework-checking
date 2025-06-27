import logging


def get_project_logger(
    name: str,
    log_level: int = 20
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
