import os

import dotenv
import prompts.generation_team as gen_team
import prompts.review_team as rev_team
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
SESSION_ID = rand.generate_session_id(CHAPTER_ID, SUBCHAPTER_ID)


def main():
    # ---------------- Prompt ----------------
    prompt_kwargs = utils.get_gen_team_prompt_kwargs(CHAPTER_ID, SUBCHAPTER_ID)
    instruction = gen_team.INSTRUCTIONS.format(**prompt_kwargs)

    # ---------------- Team 1 ----------------
    agent_instruments = FileAgentInstruments(SESSION_ID)
    course_generation_orchestrator = agents.build_team_orchestrator(
        "course_generation",
        agent_instruments,
    )

    # ------------------ Run ------------------
    course_generation_conversation_result: ConversationResult = (
        course_generation_orchestrator.sequential_conversation(instruction)
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

    utils.save_raw_course(
        SESSION_ID, course_generation_conversation_result.last_message_str
    )


def mock_review_process():
    with open(
        os.path.join(
            ".", "courses", "seconde", "maths", "raw_courses", "1703864194__c1_c1s1.md"
        )
    ) as file:
        raw_course = file.read()
    instruction = rev_team.INSTRUCTIONS.format(raw_course=raw_course)
    prompt_kwargs = None  # need to find a way to have objectives and pre-requisites
    agent_instruments = FileAgentInstruments(SESSION_ID)
    course_review_orchestrator = agents.build_team_orchestrator(
        team="course_review",
        agent_instruments=agent_instruments,
        prompt_fillers=prompt_kwargs,
    )
    # ------------------ Run ------------------
    course_review_conversation_result: ConversationResult = (
        course_review_orchestrator.broadcast_conversation(instruction)
    )
    # ----------------- Result ----------------
    match course_review_conversation_result:
        case ConversationResult(
            success=True, cost=course_gen_cost, tokens=course_gen_tokens
        ):
            print(
                f"✅ Orchestrator was successful. Team: {course_review_orchestrator.name}"
            )
            print(
                f"💰📊🤖 {course_review_orchestrator.name} Cost: {course_gen_cost}, tokens: {course_gen_tokens}"
            )
        case _:
            print(
                f"❌ Orchestrator failed. Team: {course_review_orchestrator.name} Failed"
            )


if __name__ == "__main__":
    main()
