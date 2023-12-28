import time


def generate_session_id(chapter_id: str, subchapter_id: str) -> str:
    """
    Generate a unique session ID based on the chapter and subchapter IDs.

    Args:
        chapter_id (str): The ID of the chapter.
        subchapter_id (str): The ID of the subchapter.

    Returns:
        str: A unique session ID based on the current time and the chapter and subchapter IDs.
    """
    now = time.time()
    now_int = int(now)

    raw_name = f"{chapter_id.lower()}_{subchapter_id.lower()}"
    no_spaces = raw_name.replace(" ", "")
    no_quotes = no_spaces.replace("'", "")
    with_uuid = str(now_int) + "__" + no_quotes
    return with_uuid
