from pathlib import Path

from .settings import get_application_settings
from .app.logger import get_project_logger

PACKAGE_DIR = Path(__file__).parent.resolve()

settings = get_application_settings(file_path=PACKAGE_DIR / ".env")

logger = get_project_logger(
    name=__name__, log_level=settings.DEVELOPMENT_LOG_LEVEL
)
