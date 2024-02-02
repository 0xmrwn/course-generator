from typing import List, Union

import autogen
import prompts.generation_team as gen_team
import prompts.review_team as rev_team
from agents import agents_config
from agents.instruments import FileAgentInstruments
from modules import orchestrator


# ------------------------ BUILD TEAMS ------------------------
def build_course_generation_team(
    instruments: FileAgentInstruments,
) -> List[Union[autogen.UserProxyAgent, autogen.AssistantAgent]]:
    """
    Build a team of agents that can generate a raw math course in markdown.
    """

    # create a set of agents with specific roles
    # admin user proxy agent - takes in the prompt and manages the group chat
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=gen_team.USER_PROXY_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # inspector - generates sub-chapter specs for the writer
    inspector = autogen.AssistantAgent(
        name="Inspecteur",
        llm_config=agents_config.base_config,
        system_message=gen_team.INSPECTOR_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # writer - generates raw course content based on the inspector's guidelines
    writer = autogen.AssistantAgent(
        name="Rédacteur",
        llm_config=agents_config.base_config,
        system_message=gen_team.WRITER_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    return [
        user_proxy,
        inspector,
        writer,
    ]


def build_course_review_team(
    instruments: FileAgentInstruments, fillers: dict
) -> List[Union[autogen.UserProxyAgent, autogen.AssistantAgent]]:
    """
    Build a team of agents that can review various aspects of a raw math course.
    """
    objectives = fillers["objectives"]
    prerequisites = fillers["prerequisites"]
    # create a set of agents with specific roles
    # admin user proxy agent - takes in the prompt and broadcasts to other agents
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=rev_team.USER_PROXY_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # error reviewer - reviews the course looking for errors
    logic_reviewer = autogen.AssistantAgent(
        name="Relecteur_logique",
        llm_config=agents_config.base_config,
        system_message=rev_team.LOGIC_REVIEWER,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # clarity reviewer - reviews the course looking for clarity issues
    clarity_reviewer = autogen.AssistantAgent(
        name="Relecteur_clarté",
        llm_config=agents_config.base_config,
        system_message=rev_team.CLARITY_REVIEWER,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # objective reviewer - reviews the course for objective alignment
    objective_reviewer = autogen.AssistantAgent(
        name="Relecteur_objectif",
        llm_config=agents_config.base_config,
        system_message=rev_team.OBJECTIVE_REVIEWER.format(objectives=objectives),
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # prerequisite reviewer - reviews the course for prerequisite alignment
    prerequisite_reviewer = autogen.AssistantAgent(
        name="Relecteur_pré_requis",
        llm_config=agents_config.base_config,
        system_message=rev_team.PREREQUISITES_REVIEWER.format(
            prerequisites=prerequisites
        ),
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    return [
        user_proxy,
        logic_reviewer,
        clarity_reviewer,
        objective_reviewer,
        prerequisite_reviewer,
    ]


# ------------------------ ORCHESTRATION ------------------------


def build_team_orchestrator(
    team: str,
    agent_instruments: FileAgentInstruments,
    validate_results: callable = None,
    prompt_fillers: dict = None,
) -> orchestrator.Orchestrator:
    """
    Based on a team name, build a team of agents and return an orchestrator
    """
    if team == "course_generation":
        return orchestrator.Orchestrator(
            name="course_generation_team",
            agents=build_course_generation_team(agent_instruments),
            instruments=agent_instruments,
            validate_results_func=validate_results,
        )
    elif team == "course_review":
        return orchestrator.Orchestrator(
            name="course_review_team",
            agents=build_course_review_team(agent_instruments, prompt_fillers),
            instruments=agent_instruments,
            validate_results_func=validate_results,
        )
    raise Exception("Unknown team: " + team)
