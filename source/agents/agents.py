import autogen
import prompts.generation_team as gen_team
from agents import agents_config
from agents.instruments import FileAgentInstruments
from modules import orchestrator


# ------------------------ BUILD TEAMS ------------------------
def build_course_generation_team(instruments: FileAgentInstruments):
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


# ------------------------ ORCHESTRATION ------------------------


def build_team_orchestrator(
    team: str,
    agent_instruments: FileAgentInstruments,
    validate_results: callable = None,
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
    raise Exception("Unknown team: " + team)
