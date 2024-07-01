import click


def exclusive_city_or_url(city: str, url: str) -> None:
    if city != "cunha" and url != "https://www.imprensaoficialmunicipal.com.br/cunha":
        raise click.UsageError("Cannot use --city and --url options simultaneously.")
