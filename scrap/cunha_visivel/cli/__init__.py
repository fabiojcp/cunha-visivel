from pathlib import Path
import click
from loguru import logger
import requests

from cunha_visivel.scraping import CunhaScraper
from cunha_visivel.utils.param_eval import exclusive_city_or_url
from cunha_visivel.utils.workdir import create_workdir_from_path
from cunha_visivel.workdir.operator import WorkdirOperator


# create a click cli command to download the pdfs
@click.command()
@click.option(
    "--headful",
    is_flag=True,
    help="Run the browser in headful mode",
)
@click.option(
    "--at-most",
    type=int,
    default=10,
    help="Download at most this number of PDFs",
)
@click.option(
    "--city",
    type=str,
    default="cunha",
    help="URL city path to scrape PDFs from",
)
@click.option(
    "--url",
    type=str,
    default="https://www.imprensaoficialmunicipal.com.br/cunha",
    help="full URL path to scrape PDFs from",
)
@click.option(
    "--href",
    type=str,
    default='a[href^="https://dosp.com.br/impressao.php?i="]',
    help="href button open pdf selector",
)
@click.option("--next-btn", type=str, default="a.next", help="next button selector")
@click.option(
    "--count-existing",
    is_flag=True,
    help="Skip downloading existing PDFs",
)

# add folder argument
@click.argument("workdir_path", type=click.Path())
def cunha_cli(
    headful: bool,
    workdir_path: Path,
    at_most: int,
    city: str,
    url: str,
    href: str,
    next_btn: str,
    count_existing: bool,
):
    # Ensure that only one of city or url is used
    exclusive_city_or_url(city, url)

    # Ensure the folder exists and ends with ".workdir"
    workdir_path = Path(workdir_path).absolute()
    if ".workdir" not in workdir_path.suffix:
        workdir_path = Path(str(workdir_path) + ".workdir").absolute()

    if not workdir_path.exists():
        workdir_path = create_workdir_from_path(workdir_path)

    # Start Workdir Operator
    workdir_op = WorkdirOperator(workdir_path)

    # Get all PDF links:
    pdf_links = CunhaScraper(
        headful=headful,
        city=city,
        url=url,
        href=href,
        next_btn=next_btn,
        workdir_op=workdir_op,
        count_existing=count_existing,
    ).get_pdf_links(at_most=at_most)

    for pdf_link in pdf_links:
        if pdf_link in workdir_op:
            logger.warning(f"PDF {pdf_link} exists in the workdir, skipping...")
            continue

        workdir_op.download_pdf(pdf_link)

    logger.success("Done!")


if __name__ == "__main__":
    cunha_cli()
