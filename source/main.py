import os

import dotenv
from agents import agents
from agents.instruments import FileAgentInstruments
from modules import rand, utils
from modules.types import ConversationResult

# ---------------- Your Environment Variables ----------------

dotenv.load_dotenv()

assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"


# ---------------- Constants ----------------


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
CHAPTER_ID = "C1"
SUBCHAPTER_ID = "C1S1"


def main():
    # ---------------- Prompt ----------------
    input_specs_md = utils.get_specs(SUBCHAPTER_ID)
    input_scope_md = utils.get_input_scope(CHAPTER_ID, SUBCHAPTER_ID)
    chapter_name, subchapter_name = utils.get_subchapter_identity(
        CHAPTER_ID, SUBCHAPTER_ID
    )
    prompt_kwargs = {
        "chapter_name": chapter_name,
        "subchapter_name": subchapter_name,
        "input_scope": input_scope_md,
        "input_specs": input_specs_md,
    }
    raw_prompt = """
Sous-chapitre : "{chapter_name}", faisant partie du chapitre "{subchapter_name}".

{input_scope}

---- CONTRAINTES ----
{input_specs}
    """
    prompt = raw_prompt.format(**prompt_kwargs)
    session_id = rand.generate_session_id(CHAPTER_ID, SUBCHAPTER_ID)
    agent_instruments = FileAgentInstruments(session_id)
    course_generation_orchestrator = agents.build_team_orchestrator(
        "course_generation",
        agent_instruments,
    )

    course_generation_conversation_result: ConversationResult = (
        course_generation_orchestrator.sequential_conversation(prompt)
    )

    match course_generation_conversation_result:
        case ConversationResult(
            success=True, cost=course_gen_cost, tokens=course_gen_tokens
        ):
            print(
                f"✅ Orchestrator was successful. Team: {course_generation_orchestrator.name}"
            )
            print(
                f"💰📊🤖 {course_generation_orchestrator.name} Cost: {course_gen_cost}, tokens: {course_gen_tokens}"
            )
        case _:
            print(
                f"❌ Orchestrator failed. Team: {course_generation_orchestrator.name} Failed"
            )

    # print(course_generation_conversation_result.messages[-1])


if __name__ == "__main__":
    main()
