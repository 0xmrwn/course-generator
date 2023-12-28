import time


def generate_session_id(chapter_id: str, subchapter_id: str) -> str:
    """
    "get jobs with 'Completed' or 'Started' status"

    ->

    "get_jobs_with_Completed_or_Started_status__12_22_22"
    """

    now = time.time()
    now_int = int(now)

    raw_name = f"{chapter_id.lower()}_{subchapter_id.lower()}"
    no_spaces = raw_name.replace(" ", "")
    no_quotes = no_spaces.replace("'", "")
    with_uuid = str(now_int) + "__" + no_quotes
    return with_uuid
