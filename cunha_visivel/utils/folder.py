from pathlib import Path

from loguru import logger


def create_workdir_from_path(workdir_path: Path) -> Path:
    if ".workdir" not in workdir_path.suffix:
        workdir_path = Path(str(workdir_path) + ".workdir").absolute()

    if workdir_path.exists():
        logger.info(f"Using existing workdir at {workdir_path}")
        return workdir_path

    workdir_path.mkdir()
    logger.info(f"Created workdir at {workdir_path}")
    return workdir_path
