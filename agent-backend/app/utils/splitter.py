from loguru import logger


def split_comma_separated_variable(
    values_str: str | None,
    allow_empty: bool = False,
) -> list[str]:
    """
    Split a comma-separated string into a list of trimmed non-empty values.

    Args:
        values_str: Comma-separated string such as "a@x.com,b@y.com".
        allow_empty: If True, return an empty list without warning when the
            input is empty or produces no valid values.

    Returns:
        A list of cleaned values with whitespace removed.
    """
    if values_str is None:
        if not allow_empty:
            logger.warning(
                "Expected a comma-separated string but received None."
            )
        return []

    cleaned_input = values_str.strip()
    if not cleaned_input:
        if not allow_empty:
            logger.warning(
                "Expected a comma-separated string but received an empty value."
            )
        return []

    values = [
        value.strip()
        for value in cleaned_input.split(",")
        if value.strip()
    ]

    if not values and not allow_empty:
        logger.warning(
            "Invalid comma-separated variable: '{}'. Expected at least one non-empty value.",
            values_str,
        )

    return values
