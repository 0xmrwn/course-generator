import os

import dotenv
import prompts.generation_team as gen_team
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
    prompt_kwargs = utils.get_gen_team_prompt_kwargs(CHAPTER_ID, SUBCHAPTER_ID)
    prompt = gen_team.INSTRUCTIONS.format(**prompt_kwargs)
    session_id = rand.generate_session_id(CHAPTER_ID, SUBCHAPTER_ID)

    # ---------------- Team 1 ----------------
    agent_instruments = FileAgentInstruments(session_id)
    course_generation_orchestrator = agents.build_team_orchestrator(
        "course_generation",
        agent_instruments,
    )

    # ------------------ Run ------------------
    course_generation_conversation_result: ConversationResult = (
        course_generation_orchestrator.sequential_conversation(prompt)
    )

    # ----------------- Result ----------------
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

    print("\n-------------------------------\n")
    print(course_generation_conversation_result.last_message_str)
    utils.save_raw_course(
        session_id, course_generation_conversation_result.last_message_str
    )


if __name__ == "__main__":
    main()
