import os

import yaml
from dotenv import load_dotenv
from generator import CourseGenerator

load_dotenv()
with open(os.path.join(".", "prompts.yaml")) as file:
    prompts = yaml.safe_load(file)


def main():
    chapter_id = "c1"
    subchapter_id = "c1s1"
    gen = CourseGenerator(prompts)
    gen.generate_content(chapter_id, subchapter_id)


if __name__ == "__main__":
    main()
