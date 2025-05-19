
def format_upc(upc_text):
    """
    Convert UPC to standard thirteen digit string.
    Strips whitespace from input UPC and pads with leading zeros to ensure 13 digits.
    Args:
        upc_text (str): The UPC string to format
    Returns:
        str: UPC string padded to 13 digits with leading zeros
    """

    upc_text = upc_text.strip()
    return upc_text.zfill(13)