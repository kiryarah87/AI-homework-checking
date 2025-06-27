import logging


def get_project_logger(
    name: str,
    log_level: int
) -> logging.Logger:
    """
    ПОлучает логгер с заданным именем и уровнем логирования.
    Если у логгера нет обработчиков, добавляет StreamHandler с форматтером,
    который выводит сообщения в формате: "[временная метка] уровень имя: сообщение".
    Args:
        name (str): Имя логгера.
        log_level (int): Уровень логирования (например, logging.INFO, logging.DEBUG).
    Returns:
        logging.Logger: Настроенный экземпляр логгера.
    """
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
