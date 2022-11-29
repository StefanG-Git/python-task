def get_color_code_by_number(number: int) -> str:
    """
    Gets the color code depending on the given number.

    Parameters
    ----------
    number: int
        Comparison number.

    Returns
    -------
    Color code: str
        The code of color
    """
    if number < 3:
        return "007500"
    elif number < 12:
        return "FFA500"

    return "b30000"
