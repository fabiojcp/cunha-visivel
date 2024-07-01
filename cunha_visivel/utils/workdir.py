from pathlib import Path

from loguru import logger

from cunha_visivel.workdir.structs import CunhaVisivelDB


def create_workdir_from_path(workdir_path: Path) -> Path:
    if workdir_path.exists():
        raise FileExistsError(f"Workdir already exists at {workdir_path}")

    workdir_path.mkdir()

    # Create an empty DB
    cunha_visivel_db = CunhaVisivelDB()

    db_path = workdir_path / "db.json"
    db_path.write_text(cunha_visivel_db.model_dump_json(indent=2))

    # Create dir to store PDFs
    pdf_dir = workdir_path / "pdf"
    pdf_dir.mkdir()

    logger.info(f"Created workdir at {workdir_path}")
    return workdir_path
