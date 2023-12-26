import json
import os

import yaml
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
with open(os.path.join(".", "prompts.yaml")) as file:
    prompts = yaml.safe_load(file)

subchapter = """
### C1S1: Nombres entiers
1. Nombres entiers naturels et nombres entiers relatifs
2. Multiples et diviseurs
"""

chapter_specs = """
## Utiliser les notions de multiple, diviseur et de nombre premier

### Contenus
- Notations ℕ et ℤ.
- Définition des notions de multiple, de diviseur, de nombre pair, de nombre impair.

### Capacités attendues
- Modéliser et résoudre des problèmes mobilisant les notions de multiple, de diviseur, de nombre pair, de nombre impair, de nombre premier.
- Présenter les résultats fractionnaires sous forme irréductible.

### Démonstrations
- Pour une valeur numérique de a, la somme de deux multiples de a est multiple de a.
- Le carré d'un nombre impair est impair.

### Exemples d'algorithme
- Déterminer si un entier naturel a est multiple d'un entier naturel b.
- Pour des entiers a et b donnés, déterminer le plus grand multiple de a inférieur ou égal à b.
- Déterminer si un entier naturel est premier.
"""


def extract_objectives():
    raw_sys_msg = prompts["step_1"]["system_message"]
    raw_instructions = prompts["step_1"]["instruction"]
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(raw_sys_msg)),
            HumanMessagePromptTemplate.from_template(raw_instructions),
        ]
    )
    model = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4-1106-preview", temperature=0.4
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    input_dict = {
        "chapter_name": "Nombres entiers, nombres réels",
        "subchapter": subchapter,
        "subchapter_name": "Nombres entiers",
        "chapter_specs": chapter_specs,
    }
    with get_openai_callback() as cb:
        response = chain.invoke(input_dict)
        print(response)
        print(cb)


def build_course_material():
    raw_sys_msg = prompts["step_2"]["system_message"]
    raw_instructions = prompts["step_2"]["instruction"]
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(raw_sys_msg)),
            HumanMessagePromptTemplate.from_template(raw_instructions),
        ]
    )
    model = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4-1106-preview", temperature=0.6
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    with open(os.path.join(".", "specs", "c1s1_objectives.json")) as file:
        c1s1_specs = json.load(file)
    prerequisites = c1s1_specs["prerequisites"]
    prerequisites_str = ""
    for prerequisite in prerequisites:
        prerequisites_str += f"- {prerequisite}\n"
    objectives = c1s1_specs["objectives"]
    objectives_str = ""
    for objective in objectives:
        objectives_str += f"- {objective}\n"
    input_dict = {
        "chapter_name": "Nombres entiers, nombres réels",
        "subchapter": subchapter,
        "subchapter_name": "Nombres entiers",
        "objectives": objectives_str,
        "prerequisites": prerequisites_str,
    }
    version = count_files()
    with get_openai_callback() as cb:
        response = chain.invoke(input_dict)
        with open(
            os.path.join(".", "raw_courses", f"c1s1_response_{version}.md"), "w"
        ) as file:
            file.write(response)
        print("---------")
        print(cb)


def refine_course_material():
    raw_sys_msg = prompts["step_3"]["system_message"]
    raw_instructions = prompts["step_3"]["instruction"]
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(raw_sys_msg)),
            HumanMessagePromptTemplate.from_template(raw_instructions),
        ]
    )
    model = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4-1106-preview", temperature=0.6
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    with open(os.path.join(".", "specs", "c1s1_objectives.json")) as file:
        c1s1_specs = json.load(file)

    with open(os.path.join(".", "raw_courses", "c1s1_response_0.md"), "r") as file:
        course_content = file.read()

    prerequisites = c1s1_specs["prerequisites"]
    prerequisites_str = ""
    for prerequisite in prerequisites:
        prerequisites_str += f"- {prerequisite}\n"
    objectives = c1s1_specs["objectives"]
    objectives_str = ""
    for objective in objectives:
        objectives_str += f"- {objective}\n"
    input_dict = {
        "chapter_name": "Nombres entiers, nombres réels",
        "subchapter_name": "Nombres entiers",
        "prerequisites": prerequisites_str,
        "course_content": course_content,
    }
    version = count_files()
    with get_openai_callback() as cb:
        response = chain.invoke(input_dict)
        print(response)
        with open(
            os.path.join(".", "raw_courses", f"c1s1_review_{version}.md"), "w"
        ) as file:
            file.write(response)
        print("---------")
        print(cb)


def count_files():
    directory = os.path.join(".", "raw_courses")
    file_count = len(
        [
            name
            for name in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, name))
        ]
    )
    return file_count


def main():
    # extract_objectives()
    # build_course_material()
    refine_course_material()


if __name__ == "__main__":
    main()
