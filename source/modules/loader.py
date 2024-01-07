import json
import os
import sys

import markdown_to_json
from loguru import logger

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


def md_to_json():
    base_path = os.path.join(".", "courses", "seconde", "maths", "specs", "markdown")
    output_path = os.path.join(".", "courses", "seconde", "maths", "specs", "json")
    md_files = [f for f in os.listdir(base_path) if f.endswith(".md")]
    for md_file in md_files:
        with open(os.path.join(base_path, md_file), "r") as file:
            raw_string = file.read()
        json_data = markdown_to_json.dictify(raw_string)
        json_file_name = os.path.splitext(md_file)[0] + ".json"
        json_file_path = os.path.join(output_path, json_file_name)
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=2, ensure_ascii=False)
        logger.info(f"Saved file: {json_file_name}")


if __name__ == "__main__":
    md_to_json()
