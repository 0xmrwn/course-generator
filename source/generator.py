import os

import utils
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser


class CourseGenerator:
    def __init__(self, prompts: dict) -> None:
        self.prompts = prompts
        self.model = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4-1106-preview",
            temperature=0.4,
        )
        self.output_parser = StrOutputParser()

    def _extract_objectives(self, chapter_id: str, subchapter_id: str):
        raw_sys_msg = self.prompts["step_1"]["system_message"]
        raw_instructions = self.prompts["step_1"]["instruction"]
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(raw_sys_msg)),
                HumanMessagePromptTemplate.from_template(raw_instructions),
            ]
        )
        chain = prompt | self.model | self.output_parser
        specs = utils.get_specs(subchapter_id)
        chapter_name, subchapter_name, subchapter_content = utils.get_subchapter(
            chapter_id, subchapter_id
        )
        input_dict = {
            "chapter_name": chapter_name,
            "subchapter": subchapter_content,
            "subchapter_name": subchapter_name,
            "chapter_specs": specs,
        }
        with get_openai_callback() as cb:
            response = chain.invoke(input_dict)
            print(response)
            print(cb)

    def _build_course_material(self, chapter_id: str, subchapter_id: str):
        raw_sys_msg = self.prompts["step_2"]["system_message"]
        raw_instructions = self.prompts["step_2"]["instruction"]
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(raw_sys_msg)),
                HumanMessagePromptTemplate.from_template(raw_instructions),
            ]
        )
        chain = prompt | self.model | self.output_parser
        specs = utils.get_spec_json(subchapter_id)
        chapter_name, subchapter_name, subchapter_content = utils.get_subchapter(
            chapter_id, subchapter_id
        )
        prerequisites = specs["prerequisites"]
        prerequisites_str = ""
        for prerequisite in prerequisites:
            prerequisites_str += f"- {prerequisite}\n"
        objectives = specs["objectives"]
        objectives_str = ""
        for objective in objectives:
            objectives_str += f"- {objective}\n"
        input_dict = {
            "chapter_name": chapter_name,
            "subchapter": subchapter_content,
            "subchapter_name": subchapter_name,
            "objectives": objectives_str,
            "prerequisites": prerequisites_str,
        }
        version = utils.count_files("raw_courses")
        with get_openai_callback() as cb:
            response = chain.invoke(input_dict)
            print(response)
            utils.save_markdown_output("raw_courses", version, response)
            print(cb)

    def _refine_course_material(self, chapter_id: str, subchapter_id: str):
        raw_sys_msg = self.prompts["step_3"]["system_message"]
        raw_instructions = self.prompts["step_3"]["instruction"]
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(raw_sys_msg)),
                HumanMessagePromptTemplate.from_template(raw_instructions),
            ]
        )
        chain = prompt | self.model | self.output_parser
        chapter_name, subchapter_name, _ = utils.get_subchapter(
            chapter_id, subchapter_id
        )
        specs = utils.get_spec_json(subchapter_id)
        course_content = utils.get_latest_raw_response(subchapter_id)

        prerequisites = specs["prerequisites"]
        prerequisites_str = ""
        for prerequisite in prerequisites:
            prerequisites_str += f"- {prerequisite}\n"
        objectives = specs["objectives"]
        objectives_str = ""
        for objective in objectives:
            objectives_str += f"- {objective}\n"
        input_dict = {
            "chapter_name": chapter_name,
            "subchapter_name": subchapter_name,
            "prerequisites": prerequisites_str,
            "course_content": course_content,
        }
        version = utils.count_files("reviews")
        with get_openai_callback() as cb:
            response = chain.invoke(input_dict)
            print(response)
            utils.save_markdown_output("reviews", version, response)
            print(cb)

    def generate_content(self, chapter_id: str, subchapter_id: str):
        self._extract_objectives(chapter_id, subchapter_id)
        self._build_course_material(chapter_id, subchapter_id)
        self._refine_course_material(chapter_id, subchapter_id)
